defmodule SpaceService.Carrier do
  use GenServer
  use AMQP

  require Logger

  @rabbitmq_host Application.compile_env(:space_service, :rabbitmq_host)
  @admin_exchange Application.compile_env(:space_service, :admin_exchange)
  @admin_routing_keys ["carrier", "all"]

  def start_link(services) do
    GenServer.start_link(__MODULE__, services, [])
  end

  @impl true
  def init(services) do
    Logger.info("Starting carrier with services: #{inspect(services)}")

    {:ok, conn} = Connection.open(host: @rabbitmq_host)
    {:ok, chan} = Channel.open(conn)

    :ok = Basic.qos(chan, prefetch_count: 1)

    # Service queues
    Enum.each(services, fn
      service ->
        {:ok, _info} = Queue.declare(chan, service, durable: true)
        {:ok, _consumer_tag} = Basic.consume(chan, service)
    end)

    # Admin exchange and temporary queue
    {:ok, %{queue: self_queue}} = Queue.declare(chan, "", exclusive: true)
    :ok = Exchange.declare(chan, @admin_exchange, :direct, durable: true)

    Enum.each(@admin_routing_keys, fn
      key ->
        :ok = Queue.bind(chan, self_queue, @admin_exchange, routing_key: key)
    end)

    {:ok, _consumer_tag} = Basic.consume(chan, self_queue, nil, no_ack: true)

    {:ok, chan}
  end

  @impl true
  def handle_info({:basic_consume_ok, %{consumer_tag: _consumer_tag}}, chan) do
    {:noreply, chan}
  end

  @impl true
  def handle_info({:basic_cancel, %{consumer_tag: _consumer_tag}}, chan) do
    Logger.error("Carrier was unexpectedly canceled")
    {:stop, :normal, chan}
  end

  @impl true
  def handle_info({:basic_cancel_ok, %{consumer_tag: _consumer_tag}}, chan) do
    Logger.error("Carrier was canceled")
    {:noreply, chan}
  end

  @impl true
  def handle_info({:basic_deliver, "admin=" <> message, %{routing_key: routing_key}}, chan) do
    Logger.info("Received adming message for #{inspect(routing_key)}: #{message}")
    {:noreply, chan}
  end

  @impl true
  def handle_info({:basic_deliver, payload, meta}, chan) do
    %{
      routing_key: routing_key,
      correlation_id: correlation_id,
      delivery_tag: delivery_tag,
      reply_to: reply_to
    } = meta

    Logger.info("Received #{inspect(routing_key)} job: #{payload}:#{correlation_id}")

    Basic.publish(chan, "", reply_to, "confirmation=#{payload}", correlation_id: correlation_id)
    Basic.ack(chan, delivery_tag)

    {:noreply, chan}
  end
end
