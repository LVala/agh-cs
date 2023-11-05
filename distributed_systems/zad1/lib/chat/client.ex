defmodule Chat.Client do
  @udp_data ~S"""

                ;'-.
    `;-._        )  '---.._
      >  `-.__.-'          `'.__
     /_.-'-._         _,   ^ ---)
     `       `'------/_.'----```
  """

  @mc_udp_data ~S"""

                    ,,__
        ..  ..   / o._)
       /--'/--\  \-'||
      /        \_/ / |
    .'\  \__\  __.'.'
      )\ |  )\ |
     // \\ // \\
    ||_  \\|_  \\_
    '--' '--'' '--'
  """

  def start() do
    address = Application.fetch_env!(:chat, :address)
    port = Application.fetch_env!(:chat, :port)
    multicast_address = Application.fetch_env!(:chat, :multicast_address)
    multicast_port = Application.fetch_env!(:chat, :multicast_port)

    open(address, port, multicast_address, multicast_port)
  end

  defp open(address, port, mc_address, mc_port) do
    opts = [:binary, active: false, reuseaddr: true]

    with {:ok, tcp_socket} <-
           :gen_tcp.connect(address, port, opts ++ [packet: :line]),
         {:ok, {_address, local_port}} <- :inet.sockname(tcp_socket),
         {:ok, udp_socket} <-
           :gen_udp.open(local_port, opts),
         {:ok, udp_mc_socket} <-
           :gen_udp.open(
             mc_port,
             opts ++ [ip: mc_address, add_membership: {mc_address, {0, 0, 0, 0}}]
           ) do
      Task.start_link(fn -> loop_tcp_receiver(tcp_socket) end)
      Task.start_link(fn -> loop_udp_receiver(udp_socket, local_port) end)
      Task.start_link(fn -> loop_udp_receiver(udp_mc_socket, local_port) end)

      loop_sender(
        {tcp_socket, udp_socket},
        {address, port},
        {mc_address, mc_port},
        true
      )
    else
      {:error, reason} ->
        IO.puts("Connection failed, reason: #{reason}")
        Process.exit(self(), :kill)
    end
  end

  defp loop_sender({tcp_socket, udp_socket} = sockets, addr, mc_addr, get_name?) do
    prompt = if get_name?, do: "Name: ", else: ">>> "
    data = IO.gets(prompt)

    case data do
      "\n" ->
        # dont send empty strings
        loop_sender(sockets, addr, mc_addr, get_name?)

      "U\n" when not get_name? ->
        case :gen_udp.send(udp_socket, addr, @udp_data) do
          :ok ->
            loop_sender(sockets, addr, mc_addr, get_name?)

          {:error, reason} ->
            IO.puts("Failed to send UDP data, reason: #{reason}")
            Process.exit(self(), :kill)
        end

      "M\n" when not get_name? ->
        case :gen_udp.send(udp_socket, mc_addr, @mc_udp_data) do
          :ok ->
            loop_sender(sockets, addr, mc_addr, get_name?)

          {:error, reason} ->
            IO.puts("Failed to send UDP data to multicast address, reason #{reason}")
            Process.exit(self(), :kill)
        end

      _other ->
        case :gen_tcp.send(tcp_socket, data) do
          :ok ->
            loop_sender(sockets, addr, mc_addr, false)

          {:error, reason} ->
            IO.puts("Connection terminated, reason: #{reason}")
            Process.exit(self(), :kill)
        end
    end
  end

  defp loop_tcp_receiver(socket) do
    case :gen_tcp.recv(socket, 0) do
      {:ok, data} ->
        IO.write(data)
        loop_tcp_receiver(socket)

      {:error, reason} ->
        IO.puts("TCP connection terminated, reason: #{reason}")
        Process.exit(self(), :kill)
    end
  end

  defp loop_udp_receiver(socket, local_port) do
    case :gen_udp.recv(socket, 0) do
      {:ok, {address, port, data}} ->
        # hacky
        {:ok, addresses} = :inet.getifaddrs()

        local? =
          addresses
          |> Enum.filter(fn {_id, info} -> Keyword.has_key?(info, :addr) end)
          |> Enum.map(fn {_id, info} -> Keyword.fetch!(info, :addr) end)
          |> Enum.any?(fn addr -> {addr, local_port} == {address, port} end)

        if not local?, do: IO.write(data)
        loop_udp_receiver(socket, local_port)

      {:error, reason} ->
        IO.puts("UDP datagram could not be received, reason: #{reason}")
        Process.exit(self(), :kill)
    end
  end
end
