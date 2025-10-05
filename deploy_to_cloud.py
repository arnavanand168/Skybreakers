

import os
import subprocess
import sys
from pathlib import Path

class CloudDeployer:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.app_file = "app_demo.py"

    def install_dependencies(self):

        print("📦 Installing deployment dependencies...")

        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements_flask.txt"
            ], check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False

    def prepare_for_deployment(self):

        print("🔧 Preparing project for deployment...")

        templates_dir = self.project_dir / "templates"
        templates_dir.mkdir(exist_ok=True)

        static_dir = self.project_dir / "static"
        css_dir = static_dir / "css"
        js_dir = static_dir / "js"

        css_dir.mkdir(parents=True, exist_ok=True)
        js_dir.mkdir(parents=True, exist_ok=True)

        print("✅ Project structure verified")

        if Path(self.app_file).exists():
            import shutil
            shutil.copy(self.app_file, "app.py")
            print("✅ App file prepared for deployment")

        return True

    def deploy_to_vercel(self, project_name="united-flight-dashboard"):

        print(f"\n🚀 Deploying to Vercel: {project_name}")

        try:

            result = subprocess.run(["vercel", "--version"],
                                 capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Vercel CLI not found. Please install: npm install -g vercel")
                return False

            subprocess.run([
                "vercel", "--prod",
                "--name", project_name,
                "--yes"
            ], check=True)

            print("✅ Successfully deployed to Vercel!")
            print(f"🌐 Your dashboard is live!")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Vercel deployment failed: {e}")
            return False
        except FileNotFoundError:
            print("❌ Vercel CLI not found. Install with: npm install -g vercel")
            return False

    def deploy_to_heroku(self, app_name="united-flight-dashboard"):

        print(f"\n🚀 Deploying to Heroku: {app_name}")

        try:

            result = subprocess.run(["heroku", "--version"],
                                 capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Heroku CLI not found. Please install from heroku.com")
                return False

            subprocess.run([
                "heroku", "create", app_name
            ], check=True)

            subprocess.run([
                "heroku", "config:set",
                "FLASK_ENV=production",
                "PORT=5000"
            ], check=True)

            subprocess.run([
                "git", "remote", "add", "heroku",
                f"https://git.heroku.com/{app_name}.git"
            ])

            if not Path(".git").exists():
                subprocess.run(["git", "init"], check=True)
                subprocess.run([
                    "git", "add", "."
                ], check=True)
                subprocess.run([
                    "git", "commit", "-m", "Initial commit for Heroku deployment"
                ], check=True)

            subprocess.run([
                "git", "push", "heroku", "main"
            ], check=True)

            print("✅ Successfully deployed to Heroku!")
            print(f"🌐 Your dashboard is live at: https://{app_name}.herokuapp.com")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Heroku deployment failed: {e}")
            return False
        except FileNotFoundError:
            print("❌ Heroku CLI not found. Install from heroku.com")
            return False

    def create_github_deployment(self):

        print("\n📂 Preparing GitHub deployment...")

        try:

            result = subprocess.run(["git", "--version"],
                                 capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Git not found. Please install Git first")
                return False

            if not Path(".git").exists():
                subprocess.run(["git", "init"], check=True)
                print("✅ Git repository initialized")

            gitignore_content =
        print("\n🎯 Deployment Options Available:")
        print("=" * 50)

        print("\n1. 🟢 Vercel (Recommended)")
        print("   ✅ Easy deployment")
        print("   ✅ Automatic scaling")
        print("   ✅ Custom domains")
        print("   📝 Run: npm install -g vercel && python3 deploy_to_cloud.py --vercel")

        print("\n2. 🔵 Heroku")
        print("   ✅ Python-friendly")
        print("   ✅ Add-ons available")
        print("   📝 Run: heroku login && python3 deploy_to_cloud.py --heroku")

        print("\n3. 🟡 Railway")
        print("   ✅ GitHub integration")
        print("   ✅ Easy CI/CD")
        print("   📝 Upload to GitHub, then connect at railway.app")

        print("\n4. 🟣 PythonAnywhere")
        print("   ✅ Free tier available")
        print("   ✅ Beginner friendly")
        print("   📝 Upload files manually to pythonanywhere.com")

    def run_deployment(self, platform=None, project_name=None):

        if not self.prepare_for_deployment():
            return False

        if not self.install_dependencies():
            return False

        if platform == "vercel":
            return self.deploy_to_vercel(project_name)
        elif platform == "heroku":
            return self.deploy_to_heroku(project_name)
        else:
            print("🤔 No specific platform specified. Showing options...")
            self.show_deployment_options()

            print("\n🧪 Testing local application...")
            try:
                from app_demo import analyzer
                stats = analyzer.get_dashboard_stats()
                print(f"✅ Local app working: {stats['total_flights']} flights")
                print("\n🚀 Run the app locally: python3 app_demo.py")
                print("🌐 Open: http://localhost:5000")
            except Exception as e:
                print(f"❌ Local app test failed: {e}")

            return True

def main():

    print("🛫 United Airlines Flight Difficulty Dashboard")
    print("🚀 Cloud Deployment Assistant")
    print("=" * 50)

    deployer = CloudDeployer()

    import argparse
    parser = argparse.ArgumentParser(description='Deploy Flight Dashboard')
    parser.add_argument('--platform', choices=['vercel', 'heroku'],
                       help='Platform to deploy to')
    parser.add_argument('--name', help='Project/app name')

    args = parser.parse_args()

    project_name = args.name or "united-flight-dashboard"

    success = deployer.run_deployment(args.platform, project_name)

    if success:
        print("\n🎉 Deployment process completed!")
        print("📚 For detailed instructions, see DEPLOYMENT_GUIDE.md")
    else:
        print("\n⚠️ Deployment encountered issues.")
        print("📚 Check DEPLOYMENT_GUIDE.md for troubleshooting")

if __name__ == '__main__':
    main()
