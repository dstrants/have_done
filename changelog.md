
## 2021-11-26 17:29:27
Implements todoist webhooks for a smoother integration

### Additions:
- Todoist webhooks endpoint
- Saving todoist tasks body to mongo
- Expose logging configuration


## 2021-10-19 07:28:10
### Additions
- Adds timestamps to the views of the task
  - Fixes #170
  - Fixes #169  
 

### Fixes
- Fixes gh integration formatting. Fixes #172 



## 2021-10-09 08:30:12
- ⬆️  Upgrades python dependencies
- ⬆️  Upgrades js dependencies
- 🔖  Release new version


## 2021-09-26 06:54:55
### Additions
- Adds markdown support for tasks text. Fixes #144 
- Removes the legacy formatting logic



## 2021-09-24 07:57:00
### Fixes
- ⚡️  Improves backups query performance -> Loading speed on home screen
- Fixes #134 Edit task.task closes before editting 
- 🐛  Fixes #154 Google calendar integration is brkn


## 2021-09-24 06:52:03
### Fixes
- 🐛  Fixes tiny bug on daily stand notification


## 2021-08-30 07:13:08
### Maintenance
- ⬆️  Upgrades python packages
- ⬆️  Upgrades js dependencies

### Fixes
- 🐛  Shows version inside the app Fixes #159
- 🔧  Removes admin middleware Fixes #162
- 🐛  Fixes #161
- ♻️  Refactors a loop to one-liner



## 2021-08-23 07:10:00
### Fixes
- Adds `faker` as dependency to the project to fix launching issues


## 2021-08-21 18:05:09
### Additions
- Adds a separate view for projects CRUD actions
- Adds a separate view for categories CRUD actions
- Splits the view into various files

### Fixes
- Pins `postgres-client` to `v12` to avoid image building issues
- Adds line length to deepsource configuration to reduce the noise

## 2021-07-25 18:43:40
### Fixes
- Issue with duplicate prs

## 2021-07-23 08:18:06
### Fixes
- 🐛  Fixes bug causing task projects to be None
- ♻️  Migrate targets to new format. Fixes #130


## 2021-07-23 06:41:05
### Additions
- Adds task count into defaults view. Fixes #128 

### Fixes
- Removes some debugging lines
- Refactors the way the prs are imported (`sync.tasks`) Fixes #137
- Moves github models to `sync` app
- Fixes github integration links. Fixes #135 



## 2021-07-21 18:23:22
### Fixes
- :bug: Fixes typo on PR period
- 🔧  Changes the schedule of pr import


## 2021-07-20 17:24:17
### Fixes
- 🐛  Only try to sync repositories with watch flag
- 🔧  Makes github syncs more frequent
- 🐛  Fixes github integration (merged prs)


## 2021-07-20 16:15:26
### Maintenance
- 🔧  Only push images to docker in release
- ⚰️  Removes statics configuration from nginx
- :arrow_up: Python Packages July Upgrades
- ⬆️  Upgrades yarn packages
- ➖  Removes axios


## 2021-07-20 15:29:24
### Additions
- Moves statics to scaleway bucket
- Creates a pipeline to push statics to bucket on `master` push


## 2021-07-15 08:04:36
### Fixes
- 🐛 Fixes filtering issue on slack notification Fixes wrong date filtering in daily task notification


## 2021-07-14 16:49:52
### Description
- ✨  Adds slack configuration
- 🏗️  Moves daily no tasks report to slack
- 🚧 Adds placeholder for daily report
- :sparkles: Adds daily report task


## 2021-06-17 14:19:03
### Fixes
- Fixes issue with various endpoint failing due to fields ordering

## 2021-05-18 14:45:13
### Additions
- Automatically import merged PRs. Fixes #80 
- Adds `isort` as a dev dependency

### Fixes
- Sort imports on all apps

## 2021-05-07 07:19:30
### Additions
- Automatically create tasks for sent mails. Fixes #82

### Fixes
- Moves all google functionality to sync for consistency
- Introduces the google client for consistency

## 2021-05-06 07:21:06
### Fixes
- Fixes task deletion issue on the front end. Fixes #112 

## 2021-05-06 06:47:45
### Additions
- Conditionally shows home widgets. Fixes #113 
- Introduces notification panel. Fixes #79 

## 2021-05-05 14:23:16
### Additions
- Adds fixtures. Fixes #120

### Additions
- Removes duplicate field in `Project` model

## 2021-05-05 09:34:40
### Note
**BREAKING**: From now on (`3.1.0`) tasks will only be submitted with <kbd>Enter</kbd>
### Additions
- Adds `yarn-upgrade-all` as dev dependency to easily upgrade js packages

### Fixes
- Removes helping file added during #116
- Removes stimulus controllers that were left behind during #111
- Fixes tiny issues caused by the controllers on task submit

## 2021-05-05 07:23:40
### Additions
- Task `li` element is moved to a partial
- Special view for tasks in `default` project

### Fixes
- Removes digital ocean configuration
- Fixes #117 ( _all day events breaking displaying events_ )

## 2021-04-29 09:41:30
### Additions
- Improves test coverage

## 2021-04-04 16:54:58
### Fixes
- Moves uptimerobot checks to `sync` app
- Completely removes `finance` app
- Completely removes `cloud` app
- Refactors `productivity.helpers`

## 2021-04-01 14:51:21
### Fixes
- Fixes issue with null calendar date
- Fixes issues that #105 attempted to fix. Fixes #107 
- Fixes the form of `settings.ADMINS` parameter. Fixes #110

## 2021-04-01 11:19:50
### Fixes
- Safeguards cases where the parsed task from todoist is not valid

## 2021-04-01 07:22:53
### Fixes
- Removes old debugging lines
- Fixes issue with updating tasks from past days and then being redirected to today instead of the given date

## 2021-03-31 17:07:10
### Additions
- Adds the ability to update tasks main attributes from today's view

## 2021-03-30 16:07:17
### Additions
- Adds pagination to back logs #100 

### Fixes
- Fixes issue in daily mail task filtering (for tasks)
- Makes the backup logs table mobile friendlier

## 2021-03-30 07:51:46
### Fixes
* Upgrades python packages
* Upgrade node modules
* Fixes security issue with `ssri`

## 2021-03-29 16:17:40
### Additions
* Adds a way to access the API key from the setting menu

## 2021-03-28 19:17:05
### Addition
- Creates a `log.models.Backup` each time the `sync.tasks.daily_backup` task runs


## 2021-03-26 08:27:59
### Fixes
- Reduces the size of the main image by removing some unnecessary layer
- Some improvements on the development stack
- Adds django admin static to `nginx` routing 

## 2021-03-26 07:40:05
### Fixes
- Fixes cron job schedule for daily backups

## 2021-03-25 18:40:33
### Additions
- Adds database and media backups daily

## 2021-03-23 09:11:11
### Fixes
- Fixes #86
- Tries to find a solution for #90
- Adds the redirect URL for `TaskAddonProvider`
- Adds missing docstrings `TaskAddonProvider` model.
- Fixes empty code block

## 2021-03-18 10:31:43
### Addition
- Automated weekly email report. Fixes #58

## 2021-03-18 07:42:32
### Additions
* Adds providers link to top nav

### Fixes
* Moves the providers' list view to a card layout
* Moves `simpleicons` rendering to stimulus side
* Fixes default project on events auto import


## 2021-03-15 19:05:41
### Additions
- CRUD actions fro `TaskAddonProvider` Fixes #61 
- Some touches on the daily task view
- Auto import of events to tasks Fixes #63 

### Fixes
- Fixes #70 (apps crashed when no avatar available)
- Fixes tasks delete button 

## 2021-03-12 09:22:21
### Additions
- Moves email syncing to async tasks
- Moves events syncing to async tasks

### Fixes
- Tiny display issue when the event name is big enough to consume a second row

## 2021-03-11 18:13:15
### Additions
- Delete button for tasks in daily view
- Addons to home widget -> fixes #64 
- Addons to weekly calendar -> fixes #65 
- Moves assets service to `node` service on development `docker-compose.yml`
- Weekends are hidden by default on weekly view

## 2021-03-09 07:54:07
### Additions
* A simple favicon for the app
* An avatar pic for the user

### Fixes
* Query time for `productivity.tasks.no_tasks_mail`

## 2021-03-08 17:13:22
### Additions
- adds the jira integration hook [hardcoded]


## 2021-03-08 08:47:50
### Additions
* Ability to link more than one Google accounts
* Show multiple calendars in the home widget
* Added event organizer on the calendar widget
* Get emails from multiple google accounts

### Fixes
* Redirection URL on social logins


## 2021-03-06 11:33:18
### Additions
* Adds `RedisIntegration` for `sentry-sdk`

### Fixes
* Fixes cron schedule for `productivity.tasks.no_task.mail`
* Upgrades `sentry-sdk` to to `v1.0.0.`

## 2021-03-03 10:00:07
### Description
This pr adds the first of many mail functionalities that are planned to be added to the app.

Fixes #53 

### Additions
* Adds native mailgun support through `django-anymail`
* Adds email reminder when no tasks were logged

## 2021-03-02 07:49:19
### Fixes
* This PR updates dependencies for:
  *  python packages
  *  node packages
  *  docker base image

## 2021-02-28 17:16:44
### Additions
* Adds the ability to navigate through time in daily view

### Fixes
* Fixes issue with task formatting when new tasks were added

## 2021-02-17 12:09:17
### Fixes
* Fixes tiny syntax miss

## 2021-02-17 09:41:46
### Fixes
* Fixes dates overrides on weekly calendar
* Updates yarn packages to fix #49 

## 2021-01-11 15:06:02
Bumps [axios](https://github.com/axios/axios) from 0.19.2 to 0.21.1.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/axios/axios/releases">axios's releases</a>.</em></p>
<blockquote>
<h2>v0.21.1</h2>
<h3>0.21.1 (December 21, 2020)</h3>
<p>Fixes and Functionality:</p>
<ul>
<li>Hotfix: Prevent SSRF (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3410">#3410</a>)</li>
<li>Protocol not parsed when setting proxy config from env vars (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3070">#3070</a>)</li>
<li>Updating axios in types to be lower case (<a href="https://github-redirect.dependabot.com/axios/axios/issues/2797">#2797</a>)</li>
<li>Adding a type guard for <code>AxiosError</code> (<a href="https://github-redirect.dependabot.com/axios/axios/issues/2949">#2949</a>)</li>
</ul>
<p>Internal and Tests:</p>
<ul>
<li>Remove the skipping of the <code>socket</code> http test (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3364">#3364</a>)</li>
<li>Use different socket for Win32 test (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3375">#3375</a>)</li>
</ul>
<p>Huge thanks to everyone who contributed to this release via code (authors listed below) or via reviews and triaging on GitHub:</p>
<ul>
<li>Daniel Lopretto <a href="mailto:timemachine3030@users.noreply.github.com">timemachine3030@users.noreply.github.com</a></li>
<li>Jason Kwok <a href="mailto:JasonHK@users.noreply.github.com">JasonHK@users.noreply.github.com</a></li>
<li>Jay <a href="mailto:jasonsaayman@gmail.com">jasonsaayman@gmail.com</a></li>
<li>Jonathan Foster <a href="mailto:jonathan@jonathanfoster.io">jonathan@jonathanfoster.io</a></li>
<li>Remco Haszing <a href="mailto:remcohaszing@gmail.com">remcohaszing@gmail.com</a></li>
<li>Xianming Zhong <a href="mailto:chinesedfan@qq.com">chinesedfan@qq.com</a></li>
</ul>
<h2>v0.21.0</h2>
<h3>0.21.0 (October 23, 2020)</h3>
<p>Fixes and Functionality:</p>
<ul>
<li>Fixing requestHeaders.Authorization (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3287">#3287</a>)</li>
<li>Fixing node types (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3237">#3237</a>)</li>
<li>Fixing axios.delete ignores config.data (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3282">#3282</a>)</li>
<li>Revert &quot;Fixing overwrite Blob/File type as Content-Type in browser. (<a href="https://github-redirect.dependabot.com/axios/axios/issues/1773">#1773</a>)&quot; (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3289">#3289</a>)</li>
<li>Fixing an issue that type 'null' and 'undefined' is not assignable to validateStatus when typescript strict option is enabled (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3200">#3200</a>)</li>
</ul>
<p>Internal and Tests:</p>
<ul>
<li>Lock travis to not use node v15 (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3361">#3361</a>)</li>
</ul>
<p>Documentation:</p>
<ul>
<li>Fixing simple typo, existant -&gt; existent (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3252">#3252</a>)</li>
<li>Fixing typos (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3309">#3309</a>)</li>
</ul>
<p>Huge thanks to everyone who contributed to this release via code (authors listed below) or via reviews and triaging on GitHub:</p>
<ul>
<li>Allan Cruz <a href="mailto:57270969+Allanbcruz@users.noreply.github.com">57270969+Allanbcruz@users.noreply.github.com</a></li>
<li>George Cheng <a href="mailto:Gerhut@GMail.com">Gerhut@GMail.com</a></li>
<li>Jay <a href="mailto:jasonsaayman@gmail.com">jasonsaayman@gmail.com</a></li>
<li>Kevin Kirsche <a href="mailto:Kev.Kirsche+GitHub@gmail.com">Kev.Kirsche+GitHub@gmail.com</a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/axios/axios/blob/v0.21.1/CHANGELOG.md">axios's changelog</a>.</em></p>
<blockquote>
<h3>0.21.1 (December 21, 2020)</h3>
<p>Fixes and Functionality:</p>
<ul>
<li>Hotfix: Prevent SSRF (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3410">#3410</a>)</li>
<li>Protocol not parsed when setting proxy config from env vars (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3070">#3070</a>)</li>
<li>Updating axios in types to be lower case (<a href="https://github-redirect.dependabot.com/axios/axios/issues/2797">#2797</a>)</li>
<li>Adding a type guard for <code>AxiosError</code> (<a href="https://github-redirect.dependabot.com/axios/axios/issues/2949">#2949</a>)</li>
</ul>
<p>Internal and Tests:</p>
<ul>
<li>Remove the skipping of the <code>socket</code> http test (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3364">#3364</a>)</li>
<li>Use different socket for Win32 test (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3375">#3375</a>)</li>
</ul>
<p>Huge thanks to everyone who contributed to this release via code (authors listed below) or via reviews and triaging on GitHub:</p>
<ul>
<li>Daniel Lopretto <a href="mailto:timemachine3030@users.noreply.github.com">timemachine3030@users.noreply.github.com</a></li>
<li>Jason Kwok <a href="mailto:JasonHK@users.noreply.github.com">JasonHK@users.noreply.github.com</a></li>
<li>Jay <a href="mailto:jasonsaayman@gmail.com">jasonsaayman@gmail.com</a></li>
<li>Jonathan Foster <a href="mailto:jonathan@jonathanfoster.io">jonathan@jonathanfoster.io</a></li>
<li>Remco Haszing <a href="mailto:remcohaszing@gmail.com">remcohaszing@gmail.com</a></li>
<li>Xianming Zhong <a href="mailto:chinesedfan@qq.com">chinesedfan@qq.com</a></li>
</ul>
<h3>0.21.0 (October 23, 2020)</h3>
<p>Fixes and Functionality:</p>
<ul>
<li>Fixing requestHeaders.Authorization (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3287">#3287</a>)</li>
<li>Fixing node types (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3237">#3237</a>)</li>
<li>Fixing axios.delete ignores config.data (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3282">#3282</a>)</li>
<li>Revert &quot;Fixing overwrite Blob/File type as Content-Type in browser. (<a href="https://github-redirect.dependabot.com/axios/axios/issues/1773">#1773</a>)&quot; (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3289">#3289</a>)</li>
<li>Fixing an issue that type 'null' and 'undefined' is not assignable to validateStatus when typescript strict option is enabled (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3200">#3200</a>)</li>
</ul>
<p>Internal and Tests:</p>
<ul>
<li>Lock travis to not use node v15 (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3361">#3361</a>)</li>
</ul>
<p>Documentation:</p>
<ul>
<li>Fixing simple typo, existant -&gt; existent (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3252">#3252</a>)</li>
<li>Fixing typos (<a href="https://github-redirect.dependabot.com/axios/axios/pull/3309">#3309</a>)</li>
</ul>
<p>Huge thanks to everyone who contributed to this release via code (authors listed below) or via reviews and triaging on GitHub:</p>
<ul>
<li>Allan Cruz <a href="mailto:57270969+Allanbcruz@users.noreply.github.com">57270969+Allanbcruz@users.noreply.github.com</a></li>
<li>George Cheng <a href="mailto:Gerhut@GMail.com">Gerhut@GMail.com</a></li>
<li>Jay <a href="mailto:jasonsaayman@gmail.com">jasonsaayman@gmail.com</a></li>
<li>Kevin Kirsche <a href="mailto:Kev.Kirsche+GitHub@gmail.com">Kev.Kirsche+GitHub@gmail.com</a></li>
<li>Remco Haszing <a href="mailto:remcohaszing@gmail.com">remcohaszing@gmail.com</a></li>
<li>Taemin Shin <a href="mailto:cprayer13@gmail.com">cprayer13@gmail.com</a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/axios/axios/commit/a64050a6cfbcc708a55a7dc8030d85b1c78cdf38"><code>a64050a</code></a> Releasing 0.21.1</li>
<li><a href="https://github.com/axios/axios/commit/d57cd976f3cc0f1c5bb1f0681660e50004781db5"><code>d57cd97</code></a> Updating changelog for 0.21.1 release</li>
<li><a href="https://github.com/axios/axios/commit/8b0f373df0574b7cb3c6b531b4092cd670dac6e3"><code>8b0f373</code></a> Use different socket for Win32 test (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3375">#3375</a>)</li>
<li><a href="https://github.com/axios/axios/commit/e426910be7c417bdbcde9c18cb184ead826fc0e1"><code>e426910</code></a> Protocol not parsed when setting proxy config from env vars (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3070">#3070</a>)</li>
<li><a href="https://github.com/axios/axios/commit/c7329fefc890050edd51e40e469a154d0117fc55"><code>c7329fe</code></a> Hotfix: Prevent SSRF (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3410">#3410</a>)</li>
<li><a href="https://github.com/axios/axios/commit/f472e5da5fe76c72db703d6a0f5190e4ad31e642"><code>f472e5d</code></a> Adding a type guard for <code>AxiosError</code> (<a href="https://github-redirect.dependabot.com/axios/axios/issues/2949">#2949</a>)</li>
<li><a href="https://github.com/axios/axios/commit/768825589fd0d36b64a66717ca6df2efd8fb7844"><code>7688255</code></a> Remove the skipping of the <code>socket</code> http test (<a href="https://github-redirect.dependabot.com/axios/axios/issues/3364">#3364</a>)</li>
<li><a href="https://github.com/axios/axios/commit/820fe6e41a96f05fb4781673ce07486f1b37515d"><code>820fe6e</code></a> Updating axios in types to be lower case (<a href="https://github-redirect.dependabot.com/axios/axios/issues/2797">#2797</a>)</li>
<li><a href="https://github.com/axios/axios/commit/94ca24b5b23f343769a15f325693246e07c177d2"><code>94ca24b</code></a> Releasing 0.21.0</li>
<li><a href="https://github.com/axios/axios/commit/2130a0c8acc588c72b53dfef31a11442043ffb06"><code>2130a0c</code></a> Updating changelog for 0.21.0 release</li>
<li>Additional commits viewable in <a href="https://github.com/axios/axios/compare/v0.19.2...v0.21.1">compare view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=axios&package-manager=npm_and_yarn&previous-version=0.19.2&new-version=0.21.1)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot merge` will merge this PR after your CI passes on it
- `@dependabot squash and merge` will squash and merge this PR after your CI passes on it
- `@dependabot cancel merge` will cancel a previously requested merge and block automerging
- `@dependabot reopen` will reopen this PR if it is closed
- `@dependabot close` will close this PR and stop Dependabot recreating it. You can achieve the same result by closing it manually
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)
- `@dependabot use these labels` will set the current labels as the default for future PRs for this repo and language
- `@dependabot use these reviewers` will set the current reviewers as the default for future PRs for this repo and language
- `@dependabot use these assignees` will set the current assignees as the default for future PRs for this repo and language
- `@dependabot use this milestone` will set the current milestone as the default for future PRs for this repo and language

You can disable automated security fix PRs for this repo from the [Security Alerts page](https://github.com/dstrants/backups/network/alerts).

</details>

## 2020-12-23 16:18:05
### Fixes
* Fixes an issue that prevents markup from happening

## 2020-12-23 15:55:59
### Fixed
* Removes auto-formatting re-application on filterring


## 2020-12-23 15:10:59
### Additions
* Mark `$names` as code inside tasks text

### Fixes
* Upgrades on `node_modules`

## 2020-12-10 07:31:55
### Additions
* Highlighting capitalized words
* Orders addon provider list alphabetically
* Adds new keyboard shortcut for a new task

### Fixes
* Makes the legth of `productivity.models.Task.task` 400 avoiding legth errors

## 2020-11-16 16:38:02
### Additions
* Production `docker-compose.yaml`

### Fixes
* Google oauth parameterization

## 2020-11-08 16:26:43
Adds entrypoint and cmd

## 2020-11-08 12:25:59
This PR improved the way external requests are cached. It prevents sequential calls for up to 24hrs.


## 2020-11-05 17:35:42
Tidies the CI flow

## 2020-11-02 18:11:47
### Additions
* Remove `arrow` and uses `pendulum` instead.

## 2020-11-02 18:00:20
### Additions
* Adds the ability to archive existing projects
* Update `node_modules`

### FIxes
* `STATIC_URL` missconfiguration

## 2020-11-01 14:38:12
### Additions
- Adds poetry as package manager
- Adds pydantic as configuration manager
- Tidies the env params


## 2021-01-14 17:53:57
### Additions
* Integration with todoist Sync API
* Introduction of the Profiles app

### Fixes
* `Task.task` **is not** unique anymore
* `Task.task`  `max_length=300`

## 2020-07-22 16:43:26
### Fixes
* Invoices list functionality (migrated to `stimulusjs` )

## 2020-07-13 17:23:11
### Additions
* API for addons
* API for addon providers﻿
* API today endpoint for tasks


## 2020-07-06 15:22:56
### Additions
* Adds expenses logging functionality

## 2020-06-28 18:18:06
### Fixes
* adds prefix project test
* Fixes issue with task addon short does not exist
* fixes #24 
* fixes #22 
* fixes #25 
* fixes #26 

## 2020-06-28 12:35:17
### Additions
* Adds `Category` tests
* Adds `Project` tests

### Fixes
* Removes algolia
* Removes todoist remnants

## 2020-06-19 13:57:45
### Additions
* Adds github linter

## 2020-06-19 18:27:25
### Adds
* Adds webpack to the project
* Migrates `js` to `stimulusjs`
* Migrates style to `scss`
* Removes todoist functionality
* Adds custom login page

## 2020-06-06 21:01:38
### Additions
* Ability for the app outside of Docker

## 2020-06-09 11:49:38
### Additions
* Adds rest-api endpoints for `Task`, `Project`, `Category`


## 2020-05-26 18:29:08
### Additions
* Addons functionality


## 2020-05-17 14:55:07
### Additions
* Link to edit task on admin
* Link to navigate between dates
* Weekly stats
* Moves sentry to production only

## 2020-05-16 15:55:29
### Additions
* Add ability to create and track issued invoices 

## 2020-05-06 11:37:51
### Additions
* Adds workflow to build and store the docker image to the registry

## 2020-03-02 14:23:45
### Additions 
* Adds representation for the referenced issues and PRs
* Add github oAuth 
### Fixes
* Adds prompts when no oauths 
* Shows errors on js when the occur

## 2020-02-24 17:50:55
### Additions
* Adds the ability to check coming events
* Adds the ability to filter tasks based on the project
* Adds the ability to hide tasks weekends from the week view
### Fixes
* Moves to See All (backups) button to the header and made primary for integrity
* Removes useless burger button from top nav
* Fixes on sync mails button

## 2020-02-17 16:04:55
### Additions
* Ability to check open prs in home panel
### Fixes
* Moves the mails widget to nav bar to save some space

## 2020-02-12 16:07:49
### Additions
* Small touch on `readme.md`

## 2020-02-12 17:41:01
## Additions
* Endpoint to log repo changes

## 2020-02-11 18:02:40
### Additions
* Adds Core UI as front end

## 2020-01-15 20:22:26
### Additions
* Adds functionality to check emails marked as Pending
### Fixes
* Also protects all views with  login mixin

## 2019-11-01 16:21:06
Adds cloud functionality

## 2019-10-19 16:32:26
Integrates todoist stats to the platform
