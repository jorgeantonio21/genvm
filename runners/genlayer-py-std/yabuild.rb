dev_container = find_target /runners\/cpython-dev-container$/

base_genlayer_lib_dir = cur_src.join('src')
lib_files = Dir.glob(base_genlayer_lib_dir.to_s + "/**/*.py")

compile_dir = cur_build.join('genlayer_compile_dir')
compile_dir.mkpath

out_file = compile_dir.join('compiled.zip')

build_pyc_s = target_command(
	commands: [
		['rm', '-rf', compile_dir],
		['mkdir', '-p', compile_dir],
		['cp', '-r', base_genlayer_lib_dir, compile_dir],
		[
			RbConfig.ruby, root_src.join('build-scripts', 'docker-run-in.rb'),
			'--log', cur_build.join('compile-lib-log'),
			'--id-file', dev_container.meta.output_file,
			'--out-dir', compile_dir,
			'--entrypoint', '/scripts-py/compile.sh',
			'--',
			'/out',
			'/scripts-py/save-compiled.sh', '/out/', 'compiled.zip', 'src',
		]
	],
	dependencies: [dev_container] + lib_files,
	cwd: cur_src,
	output_file: out_file,
	pool: 'console',
)

cpython_runner = find_target /runners\/cpython$/
cloudpickle_runner = find_target /runners\/py-libs\/cloudpickle$/

# extension_target = find_target /runners\/cpython-extension-lib$/

raise "Nil hash" if cpython_runner.meta.expected_hash.nil?

runner_target = target_publish_runner(
	name_base: 'genlayer-py-std',
	out_dir: config.runners_dir,
	files: [{ include: out_file }],
	runner_dict: {
		Seq: [
			{ MapFile: { to: "/py/genlayer", file: "src/" }},
			{ AddEnv: { name: "PYTHONPATH", val: "/py/genlayer" } },
			{ MapCode: { to: "/contract.py" } },
			{ SetArgs: ["py", "-u", "-c", "import contract;import genlayer.runner as r;r.run(contract)"] },
			{ Depends: cloudpickle_runner.meta.runner_dep_id },
			{ Depends: cpython_runner.meta.runner_dep_id },
		],
	},
	dependencies: [build_pyc_s],
)

target_alias(
	'genlayer-py-std',
	runner_target,
	tags: ['all', 'runner'],
	inherit_meta: ['expected_hash'],
)
