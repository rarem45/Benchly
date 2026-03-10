{ pkgs }: {
  deps = [ pkgs.python39 pkgs.python39Packages.pip ];
  # Replit will install dependencies from requirements.txt automatically.
}
