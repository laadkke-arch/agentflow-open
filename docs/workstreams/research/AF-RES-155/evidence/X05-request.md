Prettier has a breaking behavior when markdown files are used with mustache templating inside.

### Current behavior

The markdown formatter takes the initiative to remove some backticks when deemed unnecessary.

`file.md` (before code formatting):

    ````
    hello
    ````

`file.md` (after code formatting):

    ```
    hello
    ```

### Problem

This behavior becomes problematic when you insert mustache variables that contains markdown code blocks (which the formatter is not aware of):

`file.md` (before code formatting):

    ````
    {{ markdownCodeBlockSayingHello }}
    ````

`file.md` (after code formatting):

    ```
    {{ markdownCodeBlockSayingHello }}
    ```

Output after mustache rendering, resulting in a broken markdown code :

    ```
    ```
    hello
    ```
    ```

Expected output :

    ````
    ```
    hello
    ```
    ````

### Proposed fix

Extra-backticks should be preserved by default when formatting markdown:

    ````
    hello
    ````

Maybe an option could be added to remove extra backticks, but this behavior should not be enabled by default.