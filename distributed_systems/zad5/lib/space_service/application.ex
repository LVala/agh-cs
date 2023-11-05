defmodule SpaceService.Application do
  use Application

  alias SpaceService.{Admin, Agency, Carrier}

  @services Application.compile_env(:space_service, :services)

  @impl true
  def start(_type, _args) do
    # convinience for running different apps with "mix run"
    case System.get_env("APP") do
      "carrier" ->
        {:ok, _pid} = Carrier.start_link(get_services())

      "agency" ->
        Agency.start_agency()

      "admin" ->
        Admin.start_admin()

      _else ->
        raise "Invalid APP environmental variable value"
    end
  end

  defp get_services() do
    IO.puts("Supported services:")
    Enum.with_index(@services, fn elem, id -> IO.puts("    #{id}: #{elem}") end)
    IO.puts("Enter available service indicies:")
    do_get_services()
  end

  defp do_get_services(services \\ [])
  defp do_get_services(services) when length(services) == 2, do: services

  defp do_get_services(services) do
    IO.write(">>> ")

    with id <- IO.read(:line),
         id <- String.trim(id),
         {id, ""} <- Integer.parse(id),
         true <- id >= 0,
         {:ok, service} <- Enum.fetch(@services, id),
         false <- service in services do
      do_get_services([service | services])
    else
      _other ->
        IO.puts("Invalid or repeated service index, try again")
        do_get_services(services)
    end
  end
end
