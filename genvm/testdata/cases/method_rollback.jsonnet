local simple = import '../templates/simple.jsonnet';
simple.run('${jsonnetDir}/methods.py') {
    "calldata": "{\"method\": \"rback\", \"args\": []}"
}
