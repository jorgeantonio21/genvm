class CargoBuildTarget < Target
	attr_reader :output_file
	def initialize(dir, name, target, profile, features)
		@features = features
		cargo_out_dir = dir.join('target')
		@target = target
		if not target.nil?
			cargo_out_dir = cargo_out_dir.join(target)
		end
		@profile = profile
		cargo_out_dir = cargo_out_dir.join(profile)
		@cargo_out_dir = cargo_out_dir
		@dir = dir
		@is_lib = name == "lib"
		if @is_lib
			# avoid toml dependency
			File.read(@dir.join('Cargo.toml')).lines.each { |l|
				m = l.match(/name\s*=\s*"(.*)"/)
				if not m.nil?
					@name = m[1]
					break
				end
			}
			@name = 'lib' + @name.gsub('-', '_')
			suff = NATIVE_LIB_EXT
		else
			@name = name
			if @target =~ /wasm/
				suff = ".wasm"
			else
				suff = ""
			end
		end
		@output_file = @cargo_out_dir.join(@name + suff)
		super(@output_file, [dir.join('Cargo.toml')])
	end

	protected def dump_rules_impl(buf)
		buf << "  WD = #{Shellwords.escape @dir}\n"
		if @is_lib
			buf << "  FLAGS = --lib"
		else
			buf << "  FLAGS = --bin #{@name}"
		end
		if @profile != "debug"
			buf << " --profile=#{@profile}"
		end
		if @target
			buf << " --target #{@target}"
		end
		if @features.size > 0
			buf << " --features #{@features.join(',')}"
		end
		buf << "\n"
		buf << "  depfile = #{@cargo_out_dir.join(@name)}.d\n"
	end

	def mode
		"CARGO_BUILD"
	end
end

class CargoCopyTarget < Target
	def initialize(to, from, parent)
		super(to, [from])
		@parent = parent
	end

	protected def dump_rules_impl(buf)
	end

	def mode
		"COPY"
	end

	def add_deps(*deps)
		@parent.add_deps(*deps)
	end
end

add_rule(<<-EOF
rule CARGO_BUILD
  command = cd $WD && cargo build $FLAGS && touch $out
  pool = console
  description = $DESC

EOF
)

self.define_singleton_method(:target_cargo_build) do |out_file: nil, dir: nil, name:, target: nil, profile: "debug", features: [], **kwargs, &blk|
	if dir.nil?
		dir = cur_src
	end

	trg = CargoBuildTarget.new(dir, name, target, profile, features)

	if out_file.nil?
		return return_target(trg, **kwargs, &blk)
	end

	register_target(trg)

	trg_copy = CargoCopyTarget.new(out_file, trg.output_file, trg)
	return_target(trg_copy, **kwargs, &blk)
end
