defmodule SpaceService.MixProject do
  use Mix.Project

  def project do
    [
      app: :space_service,
      version: "0.1.0",
      elixir: "~> 1.14",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {SpaceService.Application, []}
    ]
  end

  defp deps do
    [
      {:amqp, "~> 3.2"}
    ]
  end
end
