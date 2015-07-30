# see config/*.service

# add to /etc/sudoers
#  production ALL=(ALL) NOPASSWD: /usr/bin/systemctl start parkapi-server@production
#  production ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop parkapi-server@production
#  production ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart parkapi-server@production
#  production ALL=(ALL) NOPASSWD: /usr/bin/systemctl status parkapi-server@production
#
#  production ALL=(ALL) NOPASSWD: /usr/bin/systemctl start parkapi-scraper@production
#  production ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop parkapi-scraper@production
#  production ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart parkapi-scraper@production
#  production ALL=(ALL) NOPASSWD: /usr/bin/systemctl status parkapi-scraper@production
#
#  staging ALL=(ALL) NOPASSWD: /usr/bin/systemctl start parkapi-server@staging
#  staging ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop parkapi-server@staging
#  staging ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart parkapi-server@staging
#  staging ALL=(ALL) NOPASSWD: /usr/bin/systemctl status parkapi-server@staging
#
#  staging ALL=(ALL) NOPASSWD: /usr/bin/systemctl start parkapi-scraper@staging
#  staging ALL=(ALL) NOPASSWD: /usr/bin/systemctl stop parkapi-scraper@staging
#  staging ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart parkapi-scraper@staging
#  staging ALL=(ALL) NOPASSWD: /usr/bin/systemctl status parkapi-scraper@staging
#
[:server, :scraper].each do |service|
  namespace service do
    [:start, :stop, :status, :restart].each do |action|
      desc "#{action} #{service}"
      task action do
        on roles(:app), in: :sequence do
          execute :sudo, "/usr/bin/systemctl", action, "parkapi-#{service}@#{fetch(:stage)}"
          if action != :status
            execute :sudo, "/usr/bin/systemctl", "status", "parkapi-#{service}@#{fetch(:stage)}"
          end
        end
      end
    end
  end
end

namespace :scraper do
  desc "show next scraper schedule"
  task :timer do
    on roles(:app) do
      execute "/usr/bin/systemctl", "list-timers"
    end
  end
end
