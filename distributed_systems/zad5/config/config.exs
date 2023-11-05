import Config

config :logger, level: :info

config :space_service,
  rabbitmq_host: "localhost",
  service_exchange: "service",
  admin_exchange: "admin",
  services: ["passenger transport", "cargo transport", "satellite launch"]
