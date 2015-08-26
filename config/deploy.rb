set :application, "ParkAPI"

role :app, %w{parkendd.higgsboson.tk}

set :scm, "git"
set :repo_url, "https://github.com/offenesdresden/ParkAPI.git"
set :branch, "master"
set :deploy_to, "/home/#{fetch(:stage)}/ParkAPI"
set :deploy_via, :remote_cache
set :keep_releases, 10
set :tmp_dir, "/tmp/Parkendd-#{fetch(:stage)}"
set :linked_files, %w{config.ini}
set :linked_dirs, %w{log}
set :shared_venv, Proc.new { shared_path.join("venv") }
set :requirements, Proc.new { release_path.join("requirements.txt") }

namespace :deploy do
  after :finishing, "deploy:cleanup"
  after :publishing, "server:restart"
  before 'deploy:updated', 'virtualenv:update'
end
