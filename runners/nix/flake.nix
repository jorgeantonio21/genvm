{
	inputs = {
		nixpkgs.url = "github:NixOS/nixpkgs/2b4230bf03deb33103947e2528cac2ed516c5c89";
	};
	outputs = inputs@{ self, nixpkgs, ... }:
		let
			pkgs = import nixpkgs {
				system = "x86_64-linux";
			};

			wasmShell = (import ./envs/wasm.nix args);
			pyShell = (import ./envs/py.nix args);
			rustShell = (import ./envs/rs.nix args);

			tools = (import ./tools args);

			runnerHashes = builtins.fromJSON (builtins.readFile ./hashes.json);

			args = {
				inherit pkgs wasmShell pyShell rustShell runnerHashes tools;
				lib = pkgs.lib;
			};
		in {
			genvm-runners-all = import ./trg args;

			genvm-make-runner = tools.genvm-make-runner;
			genvm-py-precompile = tools.genvm-py-precompile;
		};
}
