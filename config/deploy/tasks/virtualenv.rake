namespace :virtualenv do
  task :create do
    venv = fetch(:shared_venv)
    on roles(:app) do
      execute :mkdir, '-p', File.dirname(venv)
      unless test "[ -d #{venv} ]"
        execute :virtualenv, venv
      end
    end
  end

  task :pip do
    on roles(:app) do
      with(VIRTUAL_ENV: fetch(:shared_venv),
           PATH: "#{fetch(:shared_venv)}/bin:$PATH") do
        within(release_path) do
          execute "#{shared_path}/venv/bin/pip",
            "install",
            "-e", ".",
            "-r", fetch(:requirements)
        end
      end
    end
  end

  task :relocate do
    venv = fetch(:shared_venv)
    on roles(:app) do
      execute :virtualenv, "--relocatable", venv
      execute :cp, "-RPp", venv, File.join(release_path, "venv")
    end
  end

  task :update do
    invoke "virtualenv:create"
    invoke "virtualenv:pip"
    invoke "virtualenv:relocate"
  end
end
