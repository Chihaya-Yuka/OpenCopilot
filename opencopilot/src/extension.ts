import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    context.subscriptions.push(
        vscode.commands.registerCommand('openCopilot.start', () => {
            const panel = vscode.window.createWebviewPanel(
                'openCopilot',
                'OpenCopilot',
                vscode.ViewColumn.One, {
                    enableScripts: true
                }
            );

            panel.webview.html = getWebviewContent();
        })
    );

    const provider = new OpenCopilotViewProvider(context.extensionUri);

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(OpenCopilotViewProvider.viewType, provider)
    );
}

class OpenCopilotViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'openCopilot.openCopilotView';

    constructor(private readonly extensionUri: vscode.Uri) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        webviewView.webview.options = {
            enableScripts: true
        };

        webviewView.webview.html = getWebviewContent();
    }
}

function getWebviewContent() {
    const uri = 'https://awaland.xyz';
    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenCopilot</title>
</head>
<body>
<iframe src="${uri}" width="100%" height="100%" frameborder="0"></iframe>
</body>
</html>`;
}

export function deactivate() {}