namespace :log do
  desc "follow server log"
  task :tail do
    on roles(:app) do
      path = shared_path.join("log/#{fetch(:stage)}.log")
      execute "tail", "-f", path
    end
  end
end
