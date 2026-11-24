# Engineering

## Code style

Each repository contains a formatting configuration, and the formatter runs before each commit. Style discussions are settled by the configuration.

- Names describe purpose, not type.
- Functions do one thing and fit on one screen.
- Comments explain *why*, not *what*.
- Dead code is deleted, not commented out.

## Version control

```bash
git switch -c fix-login-timeout
git add -p
git commit -m "Fix timeout when the login server is slow"
git push -u origin fix-login-timeout
```

## Testing

| Level | Scope | Runs |
|-------|-------|------|
| Unit test | One function or class | On every commit |
| Integration test | Several parts together | On every merge request |
| System test | The whole product | Before every release |

::: {.callout-warning}
A failing test is never ignored. Unreliable tests are fixed or removed quickly.
:::

## Documentation

Documentation lives next to the code in plain text files and is reviewed like code. Each repository has a `README`, a short architecture description and a changelog.
