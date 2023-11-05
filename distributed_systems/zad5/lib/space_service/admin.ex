defmodule SpaceService.Admin do
  use AMQP

  @rabbitmq_host Application.compile_env(:space_service, :rabbitmq_host)
  @admin_exchange Application.compile_env(:space_service, :admin_exchange)
  @service_exchange Application.compile_env(:space_service, :service_exchange)
  @services Application.compile_env(:space_service, :services)
  @message_targets ["carrier", "agency", "all"]

  def start_admin() do
    {chan, self_queue} = setup_queues()

    {:ok, _pid} = Task.start_link(fn -> receive_messages(chan, self_queue) end)

    IO.puts("Message targets:")
    Enum.with_index(@message_targets, fn elem, id -> IO.puts("    #{id}: #{elem}") end)
    IO.puts("Enter available target index and message to send:")
    send_messages(chan, self_queue)
  end

  defp receive_messages(chan, self_queue) do
    {:ok, _consumer_tag} = Basic.consume(chan, self_queue, nil, no_ack: true)
    do_receive_messages()
  end

  defp do_receive_messages() do
    receive do
      {:basic_deliver, message, %{routing_key: routing_key, correlation_id: id}} ->
        IO.puts("Caught job request for #{inspect(routing_key)}: #{message}:#{id}")
    end

    do_receive_messages()
  end

  defp send_messages(chan, self_queue) do
    IO.write(">>> ")

    with text <- IO.read(:line),
         text <- String.trim(text),
         [id, message] <- String.split(text),
         {id, ""} <- Integer.parse(id),
         true <- id >= 0,
         {:ok, target} <- Enum.fetch(@message_targets, id) do
      Basic.publish(
        chan,
        @admin_exchange,
        target,
        "admin=#{message}",
        reply_to: self_queue,
        correlation_id: inspect(id)
      )

      IO.puts("Sent message to #{inspect(target)}: #{message}")
    else
      _other ->
        IO.puts("Invalid message description, try again")
    end

    send_messages(chan, self_queue)
  end

  defp setup_queues() do
    {:ok, conn} = Connection.open(host: @rabbitmq_host)
    {:ok, chan} = Channel.open(conn)

    # Declare temporary queue and bind to service exchange
    {:ok, %{queue: self_queue}} = Queue.declare(chan, "", exclusive: true)
    :ok = Exchange.declare(chan, @service_exchange, :direct, durable: true)

    Enum.each(@services, fn
      service ->
        :ok = Queue.bind(chan, self_queue, @service_exchange, routing_key: service)
    end)

    # Declare admin exchange
    :ok = Exchange.declare(chan, @admin_exchange, :direct, durable: true)

    {chan, self_queue}
  end
end
