{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, flake-utils, nixpkgs }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = (import nixpkgs) {
          inherit system;
        };
      in {
        devShell = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [
            poetry
            (python311.withPackages (python-pkgs: with python-pkgs; [
              argon2-cffi
              flask
              huey
              jinja2
              pytest
            ]))
            sqlite
          ];
        };
      }
    );
}
