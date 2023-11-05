defmodule Chat.Server.SocketRegister do
  use GenServer, restart: :permanent

  def start_link(_opts) do
    GenServer.start_link(__MODULE__, [], name: __MODULE__)
  end

  def add_socket(pid, addr, socket) do
    GenServer.call(__MODULE__, {:add_socket, pid, addr, socket})
  end

  def add_name(addr, name) do
    GenServer.call(__MODULE__, {:add_name, addr, name})
  end

  def get_name(addr) do
    case :ets.lookup(:names, addr) do
      [{_addr, name}] -> {:ok, name}
      [] -> {:error, :not_found}
    end
  end

  def get_other(type, my_addr) do
    :sockets
    |> :ets.tab2list()
    |> Enum.reject(fn {addr, _socket} -> my_addr == addr end)
    |> Enum.map(fn {addr, socket} -> if(type == :sockets, do: socket, else: addr) end)
  end

  @impl true
  def init(_opts) do
    :ets.new(:sockets, [:named_table, read_concurrency: true])
    :ets.new(:names, [:named_table, read_concurrency: true])
    {:ok, %{}}
  end

  @impl true
  def handle_call({:add_socket, pid, addr, socket}, _from, refs) do
    refs =
      if is_pid(pid) do
        ref = Process.monitor(pid)
        :ets.insert(:sockets, {addr, socket})
        Map.put(refs, ref, addr)
      else
        refs
      end

    {:reply, :ok, refs}
  end

  @impl true
  def handle_call({:add_name, addr, name}, _from, refs) do
    :ets.insert(:names, {addr, name})
    {:reply, :ok, refs}
  end

  @impl true
  def handle_info({:DOWN, ref, :process, _pid, _reason}, refs) do
    {addr, refs} = Map.pop(refs, ref)
    :ets.delete(:sockets, addr)
    :ets.delete(:names, addr)
    {:noreply, refs}
  end
end
