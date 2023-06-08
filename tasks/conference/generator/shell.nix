{ pkgs ? import <nixpkgs> {} }:

let
  erl = pkgs.beam.packagesWith pkgs.beam.interpreters.erlang_23;
in pkgs.stdenv.mkDerivation {

  name = "foo";

  nativeBuildInputs = [erl.erlang erl.elixir_1_10];
}
