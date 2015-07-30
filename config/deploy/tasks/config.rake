namespace :config do
  desc "Upload Configuration"
  task :upload do
    on roles(:app) do
      upload!("config.ini", shared_path.join("config.ini"))
    end
  end
end
