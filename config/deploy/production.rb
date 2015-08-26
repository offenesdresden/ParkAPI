set :branch, "stable"

server "parkendd.higgsboson.tk",
  user: "production",
  roles: %w{:app},
  port: 2222

namespace :release do
  desc "Merge master into stable, run tests"
  task :prepare do
    sh "git", "checkout", "stable"
    sh "git", "merge", "master"
    sh "python", "-m", "unittest", "discover", "tests"
  end

  desc "Push release and switch back to master"
  task :push do
    sh "git", "checkout", "stable"
    sh "git", "push", "origin"
    sh "git" "checkout", "master"
  end
end
