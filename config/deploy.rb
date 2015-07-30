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

set :slack_team, "openknowledgegermany"
set :slack_token, "xxxxxxxxxxxxxxxxxxxxxxxx"
set :slack_icon_url,         -> { "http://gravatar.com/avatar/885e1c523b7975c4003de162d8ee8fee?r=g&s=40" }
set :slack_icon_emoji,       -> { ":shipit:" }
set :slack_channel,          -> { "dresden-parkendd" }
set :slack_channel_starting, -> { nil }
set :slack_channel_finished, -> { nil }
set :slack_channel_failed,   -> { nil }
set :slack_username,         -> { "Deploybot" }
set :slack_run_starting,     -> { true }
set :slack_run_finished,     -> { true }
set :slack_run_failed,       -> { true }
set :slack_msg_starting,     -> { "#{ENV['USER'] || ENV['USERNAME']} has started deploying branch #{fetch :branch} of #{fetch :application} to #{fetch :stage}" }
set :slack_msg_finished,     -> { "#{ENV['USER'] || ENV['USERNAME']} has finished deploying branch #{fetch :branch} of #{fetch :application} to #{fetch :stage}" }
set :slack_msg_failed,       -> { "#{ENV['USER'] || ENV['USERNAME']} failed to deploy branch #{fetch :branch} of #{fetch :application} to #{fetch :stage}" }
set :slack_title_starting,   -> { nil }
set :slack_title_finished,   -> { nil }
set :slack_title_failed,     -> { nil }

namespace :deploy do
  after :finishing, "deploy:cleanup"
  after :publishing, "server:restart"
  before 'deploy:updated', 'virtualenv:update'
end
