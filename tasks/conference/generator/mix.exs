defmodule Hellojoe.MixProject do
  use Mix.Project

  def project do
    [
      app: :hellojoe,
      version: "0.1.0",
      elixir: "~> 1.10",
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      escript: escript(),
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: [:logger, :crypto]
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:typed_struct, "~> 0.3.0", runtime: false},
      {:jason, "~> 1.4"},
      {:temp, "~> 0.4"},
    ]
  end

  defp escript do
    [main_module: Hellojoe.CLI]
  end
end
