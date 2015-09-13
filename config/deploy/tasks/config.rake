namespace :config do
  desc "Upload Configuration"
  task :upload do
    on roles(:app) do
      upload!("config_#{fetch(:stage)}.ini", shared_path.join("config.ini"))
    end
  end
  task :download do
    on roles(:app) do
      download!(shared_path.join("config.ini"), "config_#{fetch(:stage)}.ini")
    end
  end
end
