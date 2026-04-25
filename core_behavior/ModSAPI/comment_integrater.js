import { readdir, readFile, stat, writeFile, appendFile } from "fs"

/**
 * 
 * @param {string} path 
 */
function transFile(path) {
    readFile(path, (err, data) => {
        if (path.indexOf(".pyi") >= 0) {
            console.log(`processing ${path}`)
            let content = data.toString();
            const lines = [];
            content.split("\n").forEach(line => {
                if (line.indexOf("from") == 0 && line.indexOf("import") > 0 && line.indexOf("typing") < 0 && line.indexOf("mod.") < 0) {
                    return;
                }
                lines.push(line);
            })
            content = "";
            lines.forEach((line) => {
                content += line;
            })
            content += "\n";
            appendFile("./indexd.pyi", content, (err) => { })
        }
        /*let msg = back;
        msg.push({ role: "user", content: data.toString() })
        const completion = await openai.chat.completions.create({
            messages: msg,
            max_completion_tokens: 64000,
            model: "deepseek-chat",
        }); 
        let target = path;
        target = target.replace("./scripts", "./output");
        target = target.replace(".js", ".py")
        let folder = target.substring(0, target.lastIndexOf("/"));
        mkdir(folder, {recursive: true}, (err) => {
            let code = completion.choices[0].message.content;
            console.log(code);
            if (code.indexOf("```") >= 0){
                code = code.substring(code.indexOf("```python") + "```python".length, code.lastIndexOf("```"))
            }
            writeFile(target, code, (err) => { });
            console.log(`file ${path} converted`);
        })*/
    })
}

function transFolder(path) {
    readdir(path, (err, files) => {
        if (err) return;
        files.forEach((file) => {
            stat(`${path}/${file}`, (err, state) => {
                if (err) console.log(err)
                if (state?.isFile()) 
                    transFile(`${path}/${file}`)
                else if (state?.isDirectory()) 
                    transFolder(`${path}/${file}`)
            })
        })
    })
}
transFolder("./")