# VS Code for Django/Wagtail development

This project illustrates the struggles of getting a basic Wagtail starter site created and then modified for use in Visual Studio Code.

While I am an experienced Django/Wagtail developer, this document describes the onboarding process for someone learning how to use Visual Studio Code for the first time who maybe doesn't have full mastery of Docker, etc.

I have yet to get VS Code working well with an existing project with a fully functioning, vanilla Docker Compose setup (borrowed from cookiecutter-django a few years back) that worked just fine without modification in PyCharm using a "remote interpreter". Too many PyCharm bugs later and I'm no longer a subscriber. I've failed to properly modify my vanilla docker-compose to play nicely with VS Code so this repo attempts to start from scratch taking a basic project and getting it to work in VS Code.

The goal is to get a project set up and working with VS Code with all the alleged benefits of using containers to isolate my host computer from any packages that may need to be installed and also getting all of the benefits of an IDE (code completion, syntax highlighting, go-to definition, debugger, etc etc).

## Install Wagtail

There is a Getting Started guide, but it says I need Python 3 as a pre-requisite.
It also says I need other stuff installed as well, but I've taken a sneak peak and see that the starter project will include a Dockerfile and I don't want to prematurely pollute my computer with packages that should only live inside a container.

So, let's get the host system bootstrapped with a working Python environment:

```
# Install homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# so you can install pyenv
brew install pyenv pyenv-virtualenv
# so you can install Python
pyenv install 3.8.13
# so you can create a virtual environment
pyenv virtualenv 3.8.13 wagtailenv
pyenv activate wagtailenv
```

Now that Python is available on the host system, time to follow Wagtail's [Getting Started](https://docs.wagtail.org/en/stable/getting_started/index.html) guide:

```
pip install wagtail
wagtail start mysite
cd mysite
```

The Getting Started docs do not show how to use the generated Dockerfile, that information is in a separate [Project Template](https://docs.wagtail.org/en/stable/reference/project_template.html) guide.

```
docker build -t mysite .
docker run -p 8000:8000 mysite
```

It seems to work! I can go to http://0.0.0.0:8000 and see the Wagtail start page. Yay!

![Wagtail Start Page, yay!](/docs/img/wagtail-start-page.png)

## Using VS Code

I hear VS Code is the new hotness that can make me productive without wasting time on getting a working development environment going.
Allegedly it can even avoid the bootstrap problem above so that I wouldn't even need python installed on my host at all.

I download VS Code and install every official Microsoft extension I can find that might be remotely related to Python development.
I open my project in VS Code and can't wait to get to work.

![VS Code - opening the project for the first time](/docs/img/vs-code-first-time-opening-the-project.png)

I consult the [official documentation](https://code.visualstudio.com/docs/) and once there, I see menu items for ["CONTAINERS"](https://code.visualstudio.com/docs/containers/overview) and see another item for ["REMOTE - CONTAINERS"](https://code.visualstudio.com/docs/remote/containers).

![Containers Menu](/docs/img/vs-docs-containers-menu.png)
![Remote Menu](/docs/img/vs-docs-remote-menu.png)

Which path should I take?

I know my project already has a Dockerfile and I know I was able to follow the Wagtail documentation to build a container from this, so "CONTAINERS" seems to be where I should start.
I skim the "Containers" overview and then head over to the [Python-specific guide](https://code.visualstudio.com/docs/containers/quickstart-python).
This guide focuses on letting VS Code create your Dockerfile and does not mention what to do if you already have a working Dockerfile.

The guide points to a sample [Django project](https://github.com/microsoft/python-sample-vscode-django-tutorial/tree/tutorial) but this also does not include an example Dockerfile or anything I might be able to borrow from.

I know the Dockerfile works from above, so maybe I can skip to the [Build, run, and debug the container](https://code.visualstudio.com/docs/containers/quickstart-python#_build-run-and-debug-the-container) section.

![No launch config](/docs/img/vs-code-no-launch-config.png)

No, I cannot because I do not have a launch.json.
I click "create a launch.json file".
I select Python as the environment:
![Python](/doc/img/vs-code-create-launch-json-01.png)

Then I select Django debug configuration:
![Django](/doc/img/vs-code-create-launch-json-02.png)

This is the result in `.vscode/launch.json`:

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver"
            ],
            "django": true,
            "justMyCode": true
        }
    ]
}
```

Hmm, that doesn't look like the one from the tutorial at all:

![Documentation example launch.json](/doc/img/python-debug-configuration.png)

The version in the Python/Django [sample repo](https://github.com/microsoft/python-sample-vscode-django-tutorial/blob/tutorial/.vscode/launch.json) also looks completely different.

Ok, so that didn't work.
Time to scroll back up to [Add Docker files to the project](https://code.visualstudio.com/docs/containers/quickstart-python#_add-docker-files-to-the-project).
It's a little confusing because "Add" doesn't mean "add existing Dockerfile so VS Code is aware of it", it means "let VS Code automatically create a Dockefile for you since you'll only ever possibly run this on a brand new project".

I use the command palette and follow the prompts:

![Step 1](/docs/img/vs-code-create-dockerfile-01.png)
![Step 2](/docs/img/vs-code-create-dockerfile-02.png)
![Step 3](/docs/img/vs-code-create-dockerfile-03.png)
![Step 4](/docs/img/vs-code-create-dockerfile-04.png)
![Step 5](/docs/img/vs-code-create-dockerfile-05.png)

When I get to the end though, my only choice is to overwrite my existing `wagtail` generated Dockerfile, the one that actually worked above.
![Overwrite your existing file, it's your only choice](/docs/img/vs-code-create-dockerfile-06.png)

I have a bad feeling about this so I `cp -R mysite mysite-backup` just in case before letting VS Code overwrite anything.

This _did_ add a "Docker: Python - Django" launch configuration so maybe I'm on the right path finally!

However, the [guide](https://code.visualstudio.com/docs/containers/quickstart-python#_gunicorn-modifications-for-django-and-flask-apps) says I must have gunicorn explicitly in my requirements.txt file and when VS Code overwrote the existing Dockerfile it deleted the included `RUN pip install "gunicorn==20.0.4"` command 🙁
Glad I made a backup!

I add `gunicorn` to `requirements.txt` and continue with the [Build, run, and debug the container](https://code.visualstudio.com/docs/containers/quickstart-python#_build-run-and-debug-the-container) guide.

I open manage.py to set a breakpoint but I'm immediately interupted with a prompt to install mypy.

![mypy alert](/docs/img/vs-code-linter-mypy-not-installed.png)

I click "x" and stay on task.

I navigate to the Run and Debug panel, select the launch config and hit F5.

It builds and runs the project and launches my browser to an error page:

![womp womp](/docs/img/vs-code-initial-launch-using-docker.png)

Ah, so when VS Code overwrote the wagtail generated Dockerfile, it erased a command that would automatically run migrations on startup.

I dig into the backups to see if I can restore some of the original Dockerfile to get this working.
There's a WARNING:

```
# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
CMD set -xe; python manage.py migrate --noinput; gunicorn mysite.wsgi:application
```

I don't want to do something that isn't a best practice so instead I add these lines to the VS Code generated Dockerfile::

    RUN python manage.py collectstatic --noinput --clear
    RUN python manage.py migrate --noinput

There's a bunch of other stuff in the Wagtail generated Dockerfile that is missing from the VS Code Dockerfile, but let's see if this is enough to get things working.

I try building again. It worked! VS Code opened up my browser to http://localhost:55001 and I see the Wagtail start page again.

I can stop the run config and start the debug config and that seems to work too, it stops on the breakpoint in `manage.py` although I cannot step into 3rd party code by default and I get reminded once again that mypy isn't installed.

![Can't step into 3rd party code](/docs/img/vs-code-cannot-step-into-3rd-party-code-by-default.png)

Ok, I'll figure that out later but this much seems to be working now.

But what about that docker-compose.yml that VS Code created?
I may want to add PostgreSQL and Redis at a minimum but let's see if the docker-compose.yml works out of the box.

I follow the [Use Docker Compose](https://code.visualstudio.com/docs/containers/docker-compose#_python) guide for Python.
It's unclear why all of this wasn't done for me when VS Code created the docker-compose.yml previously, but ok fine, I'll do it the hard way.

I navigate to launch.json in my project and click "Add Configuration".

Select "Python":
![Python](/docs/img/vs-code-create-remote-attach-config-01.png)

Select "Remote Attach":
![Remote Attach](/docs/img/vs-code-create-remote-attach-config-02.png)

Select the default host and port:
![Host](/docs/img/vs-code-create-remote-attach-config-03.png)
![Port](/docs/img/vs-code-create-remote-attach-config-04.png)

Ok, so now I have a Docker Compose run/debug launch configuration.

I follow the next steps from the documentation:

> Navigate to the Debug tab and select Python: Remote Attach as the active configuration.
> Right-click on the docker-compose.debug.yml file (example shown below) and choose Compose Up.
> Once your container is built and running, attach the debugger by hitting F5 with the Python: Remote Attach launch configuration selected.

Nothing happens. I see that VS Code brought up the docker-compose container but it doesn't launch a browser and http://0.0.0.0:8000 is not working.

I notice that `launch.json` has `"remoteRoot": "."` but I see that the Dockerfile that VS Code generated sets the working directory to "/app", so let's change that to `"remoteRoot": "/app"`. Again, VS Code defined all of this so its unclear why it would auto-generate incompatible settings, but easy enough to fix manually.

I right click on the debug.yml and do a "Compose Down" followed by a "Compose Up" and then run the debug launch config again.
It works! I'm back in my breakpoint in manage.py.

However, VS Code is has lost its intelligence, there are squigly lines under import statements as if there is an error or problem.

![Squiglies gonna get you](/docs/img/vs-code-docker-compose-no-intelligence-01.png)
![reportMissingImport](/docs/img/vs-code-docker-compose-no-intelligence-02.png)

I decide to get rid of that annoying `mypy` warning and let VS Code install.
Wait what? It installed on my host computer and for some reason picked the `homebrew` installed Python:

```
/usr/local/opt/python@3.9/bin/python3.9 -m pip install -U mypy
mysite$ /usr/local/opt/python@3.9/bin/python3.9 -m pip install -U mypy
DEPRECATION: Configuring installation scheme with distutils config files is deprecated and will no longer work in the near future. If you are using a Homebrew or Linuxbrew Python, please see discussion at https://github.com/Homebrew/homebrew-core/issues/76621
Collecting mypy
Downloading mypy-0.942-cp39-cp39-macosx_10_9_x86_64.whl (10.6 MB)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.6/10.6 MB 30.1 MB/s eta 0:00:00
Collecting tomli>=1.1.0
Using cached tomli-2.0.1-py3-none-any.whl (12 kB)
Collecting typing-extensions>=3.10
Using cached typing_extensions-4.1.1-py3-none-any.whl (26 kB)
Collecting mypy-extensions>=0.4.3
Using cached mypy_extensions-0.4.3-py2.py3-none-any.whl (4.5 kB)
Installing collected packages: mypy-extensions, typing-extensions, tomli, mypy
DEPRECATION: Configuring installation scheme with distutils config files is deprecated and will no longer work in the near future. If you are using a Homebrew or Linuxbrew Python, please see discussion at https://github.com/Homebrew/homebrew-core/issues/76621
DEPRECATION: Configuring installation scheme with distutils config files is deprecated and will no longer work in the near future. If you are using a Homebrew or Linuxbrew Python, please see discussion at https://github.com/Homebrew/homebrew-core/issues/76621
DEPRECATION: Configuring installation scheme with distutils config files is deprecated and will no longer work in the near future. If you are using a Homebrew or Linuxbrew Python, please see discussion at https://github.com/Homebrew/homebrew-core/issues/76621
DEPRECATION: Configuring installation scheme with distutils config files is deprecated and will no longer work in the near future. If you are using a Homebrew or Linuxbrew Python, please see discussion at https://github.com/Homebrew/homebrew-core/issues/76621
DEPRECATION: Configuring installation scheme with distutils config files is deprecated and will no longer work in the near future. If you are using a Homebrew or Linuxbrew Python, please see discussion at https://github.com/Homebrew/homebrew-core/issues/76621
Successfully installed mypy-0.942 mypy-extensions-0.4.3 tomli-2.0.1 typing-extensions-4.1.1
```

However, my system Python is configured by pyenv::

```
$ which python
/Users/username/.pyenv/shims/python
$ python --version
Python 3.8.13
```

So while I can run the project using docker-compose, it appears VS Code has zero intelligence about the actual Python environment in the container, it is looking hopelessly at my host system and as a result can't resolve any import statements and will only make matters worse if I continue to respond to VS Code's prompts to install more stuff, polluting my host system.

I don't see a way forward of how to smarten VS Code up to use the interpreter in the container so this looks like a dead end.

## Maybe dev containers are the answer?

From the [Overview](https://code.visualstudio.com/docs/remote/remote-overview):

![The Dev Container promise](/docs/img/vs-code-the-dev-container-promise.png)

From [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers)

> This lets VS Code provide a local-quality development experience including full IntelliSense (completions), code navigation, and debugging regardless of where your tools (or code) are located.

Sounds great!

From [Quick start: Open an existing folder in a container](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-an-existing-folder-in-a-container), I use the Command Palette to "Remote Container: Open Folder in Container..."

![Remote Container: Open Folder in Container...](/docs/img/remote-container-open-folder-01.png)

Reuse the existing debug compose file:

![docker-compose.debug.yml](/docs/img/remote-container-open-folder-02.png)

It relaunches VS Code but now I have to wait for it start the dev container and in the meantime, I can't use the editor at all or even browse files:

![Can't interact while starting](/docs/img/remote-container-open-folder-03.png)

Ok, it's done building and I can see my project again.
Time to hit that run config and see what happens.

![womp womp](/docs/img/dev-container-cannot-run-existing-launch-config-01.png)

I navigate to my `launch.json` and see squiglies:

![womp womp](/docs/img/dev-container-cannot-run-existing-launch-config-02.png)

I have no clue what to do now, but I'm starting to get a hunch that this crazy VS Code/container nesting doll I've found myself in only has VS Code Python extensions installed in the host version of VS Code but not the version of VS Code that is running in the dev container.
A bunch of documentation reading later I see that I can update my `devcontainer.json` from this:

```
"extensions": []
```

To this:

```
"extensions": [
    "ms-azuretools.vscode-docker",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "batisteo.vscode-django",
]
```

I use the Command Palette to rebuild the dev container.

![womp womp](/docs/img/dev-container-cannot-run-existing-launch-config-03.png)

Hmm, ok so maybe I shouldn't be using that Remote Attach config because now VS Code is already running in the container where the Python/Wagtail container is running so maybe just use the previously created "Python Django" localhost-styel launch config.

That seems to work in that it starts `runserver` but it's saying I've got to apply the migrations. 
Didn't I just do this in the Dockerfile a little bit ago?

![womp womp](/docs/img/dev-container-cannot-run-existing-launch-config-04.png)

I open a new terminal, in the running container and apply the migrations with `python manage.py migrate`.

I can now get the Wagtail start page in my browser!

Let's see if debugging still works.
I open manage.py to make sure I still have my breakpoint in place when I get a visit from an old friend:

![mypy not installed](/docs/img/vs-code-linter-mypy-not-installed-pt-2.png)

Alright VS Code, let's try this again and see if you install in the correct place:

```
appuser@e7bc9d1c78d7:/workspace$ /usr/local/bin/python3 -m pip install -U mypy
Defaulting to user installation because normal site-packages is not writeable
Collecting mypy
  Downloading mypy-0.942-cp38-cp38-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_12_x86_64.manylinux2010_x86_64.whl (16.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.8/16.8 MB 24.6 MB/s eta 0:00:00
Collecting typing-extensions>=3.10
  Downloading typing_extensions-4.1.1-py3-none-any.whl (26 kB)
Collecting mypy-extensions>=0.4.3
  Downloading mypy_extensions-0.4.3-py2.py3-none-any.whl (4.5 kB)
Collecting tomli>=1.1.0
  Downloading tomli-2.0.1-py3-none-any.whl (12 kB)
Installing collected packages: mypy-extensions, typing-extensions, tomli, mypy
  WARNING: The scripts dmypy, mypy, mypyc, stubgen and stubtest are installed in '/home/appuser/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed mypy-0.942 mypy-extensions-0.4.3 tomli-2.0.1 typing-extensions-4.1.1
```

Success! Sort of! Besides some warnings that I'm not sure if I can ignore but gosh, I'd really like to get work on my new Wagtail site so let's move on for now.

I start the debugger using the "Python: Django" launch config and it hits my breakpoint in `manage.py`!

I check in on models.py to see if VS Code has regained its intelligence.
Well lookie there, no squiglies!

![no squiglies](/docs/img/vs-code-docker-compose-regains-intelligence-01.png)

Heck, I can even "Go to Definition"!

![go to definition works](/docs/img/vs-code-docker-compose-regains-intelligence-02.png)


## Running Tests with VS Code

Is it possible? Dare I try?
I add a tests.py in the home folder.

![black is not installed](/docs/img/black-is-not-installed.png)

Yay! Another prompt from VS Code! 
Fine VS Code, go ahead and install.
Oh, that same warning again but I'll ignore like last time.

```
WARNING: The scripts black and blackd are installed in '/home/appuser/.local/bin' which is not on PATH.
Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

I add the simplest test that should work in `home/tests.py`:

```python
from django.test import TestCase


class HomeTestCase(TestCase):
    def test_number_one(self):
        self.assertEqual(1, 1)

```

I'm not sure how to run tests in VS Code.
In PyCharm there is a run/debug icon in the gutter next to each detected test class and method.
I see a flask icon with "Testing" as the hover text, so I check it out.

Ah, I have to configure Python tests first.

![configure test runner](/docs/img/configure-python-tests-01.png)

I'm given two options for testing, unittest and pytest.
I know Django's tests extends unittest, so I select that:

![unittest](/docs/img/configure-python-tests-02.png)
![unittest args](/docs/img/configure-python-tests-03.png)

I see that it added some stuff to `.vscode/settings.json` so maybe I've got to rebuild the dev container again?
I wait for it to rebuild but am prompted yet again to reload the window:

![pylance reload](/docs/img/pylance-reload-window.png)

For goodness' sake:

![mypy is not installed](/docs/img/vs-code-linter-mypy-not-installed-pt-3.png)

```
appuser@c04db3050f37:/workspace$ /usr/local/bin/python3 -m pip install -U mypy
Defaulting to user installation because normal site-packages is not writeable
Collecting mypy
  Downloading mypy-0.942-cp38-cp38-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_12_x86_64.manylinux2010_x86_64.whl (16.8 MB)
     ━━━━━━ 16.8/… 26.1   eta 0:00:…
            MB     MB/s             
Collecting tomli>=1.1.0
  Downloading tomli-2.0.1-py3-none-any.whl (12 kB)
Collecting typing-extensions>=3.10
  Downloading typing_extensions-4.1.1-py3-none-any.whl (26 kB)
Collecting mypy-extensions>=0.4.3
  Downloading mypy_extensions-0.4.3-py2.py3-none-any.whl (4.5 kB)
Installing collected packages: mypy-extensions, typing-extensions, tomli, mypy
  WARNING: The scripts dmypy, mypy, mypyc, stubgen and stubtest are installed in '/home/appuser/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed mypy-0.942 mypy-extensions-0.4.3 tomli-2.0.1 typing-extensions-4.1.1
```

Apparently every time VS Code rebuilds the dev container it loses any packages VS Code itself installed (no persistent volume?), so I add this to requirements.txt to hopefully silence these alerts once and for all:

```
black
mypy
```

I rebuild the container once more.
Oh hi pylance, sure why not:

![pylance reload](/docs/img/pylance-reload-window.png)

Ok, so I finally am able to see my tests in the Testing panel and I finally see icons in the gutter for running/debugging.
I click the run button, but it fails out of the box:

```
django.core.exceptions.ImproperlyConfigured: Requested setting DATABASES, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.
```

Ah, so VS Code can only run standard unittests but isn't smart enough despite all the Django configuration here that it needs to run `python manage.py test...`.

The VS Code [Django tutorial](https://code.visualstudio.com/docs/python/tutorial-django) specifically punts on the the topic of testing:

> There are also the files apps.py (app configuration), admin.py (for creating an administrative interface), and **tests.py (for creating tests), which are not covered here**.

A bunch of searching later, it turns out VS Code only partially supports Django, it does not support [running tests](https://github.com/microsoft/vscode-python/issues/73) using the `manage.py test` runner.

For now, this limitation requires adding this workaround boilerplate to every single test file in my project:

```python
import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")
django.setup()
```

Clunky, and not something I'd want to do for a large existing project but for a new project, it's at least possible to get VS Code to run/debug your tests without too much trouble.

6-8 hours later, I think I can start building my new Wagtail site with VS Code.
