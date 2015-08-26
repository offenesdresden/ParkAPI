set :branch, "stable"

server "parkendd.higgsboson.tk",
  user: "production",
  roles: %w{:app},
  port: 2222

namespace :release do
  desc "Merge master into stable, run tests"
  task :prepare do
    remotes = %x[git remote].split(/\n/)
    unless remotes.include?("offenesdresden")
      sh "git", "remote", "add", "offenesdresden", "git@github.com/offenesdresden/ParkAPI.git"
    end
    sh "git", "checkout", "stable"
    sh "git", "pull", "offenesdresden", "stable"
    sh "git", "merge", "master"
    sh "python", "-m", "unittest", "discover", "tests"
    sh "python", "tests/validate-geojson.py", *Dir.glob("park_api/cities/*.geojson")
  end

  desc "Push release and switch back to master"
  task :push do
    sh "git", "checkout", "stable"
    sh "git", "push", "offenesdresden", "stable"
    sh "git" "checkout", "master"
  end
end
