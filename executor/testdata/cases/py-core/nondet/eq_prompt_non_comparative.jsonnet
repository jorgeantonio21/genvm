local simple = import 'templates/simple.jsonnet';
simple.run('${jsonnetDir}/eq_prompt_non_comparative.py') {
    "calldata": |||
        {
            "method": "main",
            "args": []
        }
    |||
}
