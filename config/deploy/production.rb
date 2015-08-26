set :branch, "stable"

server "parkendd.higgsboson.tk",
  user: "production",
  roles: %w{:app},
  port: 2222

namespace :release do
  def ensure_remote
    remotes = %x[git remote].split(/\n/)
    unless remotes.include?("offenesdresden")
      sh "git", "remote", "add", "offenesdresden", "git@github.com:offenesdresden/ParkAPI.git"
      sh "git", "fetch", "offenesdresden", "stable"
    end
  end

  desc "Merge master into stable, run tests"
  task :prepare do
    ensure_remote
    sh "git", "checkout", "stable"
    sh "git", "pull", "offenesdresden", "stable"
    sh "git", "merge", "master"
    sh "python", "-m", "unittest", "discover", "tests"
    sh "python", "tests/validate-geojson.py", *Dir.glob("park_api/cities/*.geojson")
    puts "HINT: hard reset last merge"
    puts "$ cap #{fetch(:stage)} release:reset"
  end

  desc "Reset stable branch to offenesdresden/stable HARD"
  task :reset do
    ensure_remote
    sh "git", "checkout", "stable"
    sh "git", "stash", "save"
    sh "git", "reset", "--hard", "offenesdresden/stable"
    sh "git", "checkout", "master"
  end

  desc "Push release and switch back to master"
  task :push do
    ensure_remote
    sh "git", "checkout", "stable"
    sh "git", "push", "offenesdresden", "stable"
    sh "git", "checkout", "master"
  end
end
