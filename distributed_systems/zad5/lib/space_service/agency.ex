defmodule SpaceService.Agency do
  use AMQP

  @rabbitmq_host Application.compile_env(:space_service, :rabbitmq_host)
  @admin_exchange Application.compile_env(:space_service, :admin_exchange)
  @service_exchange Application.compile_env(:space_service, :service_exchange)
  @services Application.compile_env(:space_service, :services)
  @admin_routing_keys ["agency", "all"]

  def start_agency() do
    {chan, self_queue} = setup_queues()

    {:ok, _pid} = Task.start_link(fn -> receive_messages(chan, self_queue) end)

    IO.puts("Pass agency name: ")
    IO.write(">>> ")
    name = IO.read(:line) |> String.trim()

    IO.puts("Supported services:")
    Enum.with_index(@services, fn elem, id -> IO.puts("    #{id}: #{elem}") end)
    IO.puts("Enter available service index and job name to send message:")
    send_messages(chan, self_queue, name, 0)
  end

  defp receive_messages(chan, self_queue) do
    {:ok, _consumer_tag} = Basic.consume(chan, self_queue, nil, no_ack: true)
    do_receive_messages()
  end

  defp do_receive_messages() do
    receive do
      {:basic_deliver, "admin=" <> message, %{routing_key: routing_key}} ->
        IO.puts("Received admin message for #{inspect(routing_key)}: #{message}")

      {:basic_deliver, "confirmation=" <> name, %{correlation_id: correlation_id}} ->
        IO.puts("Received confirmation for job #{name}:#{correlation_id}")
    end

    do_receive_messages()
  end

  defp send_messages(chan, self_queue, name, cor_id) do
    IO.write(">>> ")

    cor_id =
      with text <- IO.read(:line),
           text <- String.trim(text),
           {id, ""} <- Integer.parse(text),
           true <- id >= 0,
           {:ok, service} <- Enum.fetch(@services, id) do
        Basic.publish(
          chan,
          @service_exchange,
          service,
          name,
          reply_to: self_queue,
          correlation_id: inspect(cor_id)
        )

        IO.puts("Sent job request #{name}:#{cor_id}")
        cor_id + 1
      else
        _other ->
          IO.puts("Invalid job description, try again")
          cor_id
      end

    send_messages(chan, self_queue, name, cor_id)
  end

  defp setup_queues() do
    {:ok, conn} = Connection.open(host: @rabbitmq_host)
    {:ok, chan} = Channel.open(conn)

    # Setup service exchange and queues
    :ok = Exchange.declare(chan, @service_exchange, :direct, durable: true)

    Enum.each(@services, fn
      service ->
        {:ok, _info} = Queue.declare(chan, service, durable: true)
        :ok = Queue.bind(chan, service, @service_exchange, routing_key: service)
    end)

    # Admin exchange and temporary queue
    {:ok, %{queue: self_queue}} = Queue.declare(chan, "", exclusive: true)
    :ok = Exchange.declare(chan, @admin_exchange, :direct, durable: true)

    Enum.each(@admin_routing_keys, fn
      key ->
        :ok = Queue.bind(chan, self_queue, @admin_exchange, routing_key: key)
    end)

    {chan, self_queue}
  end
end
