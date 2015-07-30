set :branch, "stable"

server "parkendd.higgsboson.tk",
  user: "production",
  roles: %w{:app},
  port: 2222
