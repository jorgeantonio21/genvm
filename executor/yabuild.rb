project('executor') {
	modules_dir = config.out_dir.join('lib', 'genvm-modules')

	base_env = {}
	compiler = config.tools.clang || config.tools.gcc
	linker = config.tools.mold || config.tools.lld

	if config.executor_target.nil? and not compiler.nil? and not linker.nil?
		base_env['RUSTFLAGS'] ||= ''
		base_env['RUSTFLAGS'] << "-Clinker=#{Shellwords.escape compiler} -Clink-arg=-fuse-ld=#{Shellwords.escape linker}"
	end

	if config.executor.coverage
		base_env['RUSTFLAGS'] ||= ''
		base_env['RUSTFLAGS'] << " -Cinstrument-coverage"
	end

	base_env['RUSTFLAGS'] ||= ''
	base_env['RUSTFLAGS'] << ' -C target-feature=+crt-static'

	cargo_flags = []
	if not config.executor_target.nil?
		linker_path = root_src.join('build-scripts', 'zig-driver.py')
		cargo_flags << '--config' << "target.#{config.executor_target}.linker=\"#{linker_path.to_s}\""
		base_env['CC_aarch64_unknown_linux_gnu'] = linker_path.to_s
		base_env['AARCH64_UNKNOWN_LINUX_GNU_OPENSSL_LIB_DIR'] = root_src.join('tools/downloaded/cross-aarch64-libs/usr/lib/openssl-1.0').to_s
		base_env['AARCH64_UNKNOWN_LINUX_GNU_OPENSSL_INCLUDE_DIR'] = root_src.join('tools/downloaded/cross-aarch64-libs/usr/include/openssl-1.0').to_s
	end

	run_codegen = Proc.new { |inp, out, type:, tags: [], **kwargs, &blk|
		if type == "rs"
			script = cur_src.join('codegen', 'templates', 'rs.rb')
		elsif type == "py"
			script = cur_src.join('codegen', 'templates', 'py.rb')
		else
			raise "unknown type #{type}"
		end
		target_command(
			output_file: out,
			command: [
				RbConfig.ruby, script, inp, out,
			],
			dependencies: [inp, script],
			tags: ['codegen'] + tags,
			**kwargs, &blk
		)
	}

	codegen = target_alias(
		"codegen",
		run_codegen.(cur_src.join('codegen', 'data', 'host-fns.json'), cur_src.join('src', 'host', 'host_fns.rs'), type: "rs"),
		run_codegen.(cur_src.join('codegen', 'data', 'result-codes.json'), cur_src.join('src', 'host', 'result_codes.rs'), type: "rs"),
		run_codegen.(cur_src.join('codegen', 'data', 'builtin-prompt-templates.json'), cur_src.join('modules', 'implementation', 'llm-funcs', 'src', 'template_ids.rs'), type: "rs"),
	)

	genvm_id_path = root_build.join('genvm_id.txt')
	gen_id = target_command(
		output_file: cur_build.join('genvm_id.trg'),
		command: [
			RbConfig.ruby, root_src.join('build-scripts', 'generate-id.rb'), root_src, genvm_id_path.relative_path_from(root_build)
		],
		dependencies: [],
		cwd: root_build,
		tags: ['all'],
	)

	base_env['GENVM_PROFILE_PATH'] = genvm_id_path.relative_path_from(cur_src)

	gen_id_first = target_command(
		output_file: genvm_id_path,
		command: [
			RbConfig.ruby, root_src.join('build-scripts', 'generate-id.rb'), root_src, genvm_id_path.relative_path_from(root_build)
		],
		dependencies: [],
		cwd: root_build,
	)

	bin = target_alias(
		'bin',
		target_cargo_build(
			name: "genvm",
			target: config.executor_target,
			profile: config.profile,
			out_file: config.bin_dir.join('genvm'),
			flags: cargo_flags,
			env: base_env,
		) {
			inputs.push(codegen, gen_id_first)
		}
	)

	config_target = target_copy(
		dest: config.out_dir.join('share', 'genvm', 'default-config.json'),
		src: [cur_src.join('default-config.json')],
	)

	genvm_all = target_alias('all', bin, config_target, tags: ['all'])

	run_codegen.(cur_src.join('codegen', 'data', 'host-fns.json'), cur_src.join('testdata', 'runner', 'host_fns.py'), type: "py", tags: ['testdata'])
	run_codegen.(cur_src.join('codegen', 'data', 'result-codes.json'), cur_src.join('testdata', 'runner', 'result_codes.py'), type: "py", tags: ['testdata'])
}
