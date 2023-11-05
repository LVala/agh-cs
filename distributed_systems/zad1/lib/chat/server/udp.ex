defmodule Chat.Server.UDP do
  require Logger

  alias Chat.Server.SocketRegister

  def open(port) do
    case :gen_udp.open(port, [:binary, active: false, reuseaddr: true]) do
      {:ok, socket} ->
        Logger.info("Listening for UDP data on port #{port}")
        serve(socket)

      {:error, reason} ->
        Logger.error("Unable to receive UDP data on port #{port}, reason: #{reason}")
    end
  end

  defp serve(socket) do
    case :gen_udp.recv(socket, 0) do
      {:ok, {address, port, data}} ->
        Logger.info("Received message via UDP")

        name =
          case SocketRegister.get_name({address, port}) do
            {:ok, name} ->
              name

            {:error, :not_found} ->
              Logger.warn("Could not find the name of UDP datagram sender")
              "Unknown"
          end

        :addresses
        |> SocketRegister.get_other({address, port})
        |> Enum.each(fn addr ->
          case :gen_udp.send(socket, addr, "#{name}: #{data}") do
            :ok ->
              :ok

            {:error, reason} ->
              Logger.error("Failed to send UDP datagram, reason: #{reason}")
          end
        end)

        serve(socket)

      {:error, reason} ->
        Logger.warn("Unable to receive data via UDP, reson: #{reason}")
    end
  end
end
