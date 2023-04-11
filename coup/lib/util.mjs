const assert = (value, msg) => {
    if (!value) {
        throw new Error(msg);
    }
}

export { assert }