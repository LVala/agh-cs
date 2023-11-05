defmodule Chat.Server.TCP do
  require Logger

  alias Chat.Server.SocketRegister

  def accept(port) do
    case :gen_tcp.listen(port, [:binary, packet: :line, active: false, reuseaddr: true]) do
      {:ok, socket} ->
        Logger.info("Accepting TCP connections on port #{port}")
        loop_acceptor(socket)

      {:error, reason} ->
        Logger.warn("Unable to listen for TCP connections on port #{port}, reason: #{reason}")
    end
  end

  defp loop_acceptor(socket) do
    with {:ok, client} <- :gen_tcp.accept(socket),
         {:ok, {address, port} = addr} <- :inet.peername(client) do
      Logger.info("Accepted TCP connection from #{address_to_string(address)}:#{port}")

      {:ok, pid} =
        Task.Supervisor.start_child(Chat.Server.SocketSupervisor, fn -> serve(client) end)

      :ok = :gen_tcp.controlling_process(client, pid)
      :ok = SocketRegister.add_socket(pid, addr, client)
      loop_acceptor(socket)
    else
      {:error, reason} -> Logger.warn("Unable to accept TCP connections, reason: #{reason}")
    end
  end

  defp serve(socket) do
    with {:ok, data} <- :gen_tcp.recv(socket, 0),
         {:ok, {address, port} = addr} <- :inet.peername(socket) do
      Logger.info("Received message via TCP from #{address_to_string(address)}:#{port}")

      case SocketRegister.get_name(addr) do
        {:ok, name} ->
          :sockets
          |> SocketRegister.get_other(addr)
          |> Enum.each(fn client ->
            case :gen_tcp.send(client, "#{name}: #{data}") do
              :ok ->
                :ok

              {:error, reason} ->
                Logger.warn(
                  "Failed to send the message from #{address_to_string(address)}:#{port}, reason: #{reason}"
                )
            end
          end)

        {:error, :not_found} ->
          SocketRegister.add_name(addr, String.trim(data, "\n"))
      end

      serve(socket)
    else
      {:error, reason} ->
        Logger.warn("Connection terminated, reason: #{reason}")
    end
  end

  defp address_to_string({oct1, oct2, oct3, oct4}) do
    "#{oct1}.#{oct2}.#{oct3}.#{oct4}"
  end
end
