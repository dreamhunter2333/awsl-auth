interface Window {
    ethereum: {
        request: (args) => Promise<string[]>;
    };
}
