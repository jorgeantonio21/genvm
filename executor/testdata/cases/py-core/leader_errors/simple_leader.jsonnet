local simple = import 'templates/simple.jsonnet';
simple.run('${jsonnetDir}/simple.py') {
    "calldata": |||
        {
            "method": "foo",
            "args": []
        }
    |||
}
