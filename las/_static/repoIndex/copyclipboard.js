function new_exp_copyclipboard_ssh(str) {
  function listener(e) {
    e.clipboardData.setData("text/html", str);
    e.clipboardData.setData("text/plain", str);
    e.preventDefault();
  }
 // username@hostname/home/username/path/5db6ffb4495575f385b70150
  // ssh -t username@hostname "cd /path; bash"
  var host = str.substr(0, str.indexOf('/'))
  var path = str.substring(str.indexOf('/')+1)
  var ssh_string = "ssh -t " + host + " \"cd " + path + "; bash\""
  console.log("ssh_string is: ", ssh_string)
  var clip_ssh = document.createElement("input")
  document.body.appendChild(clip_ssh);
  clip_ssh.setAttribute("id", "clip_ssh_id");
  document.getElementById("clip_ssh_id").value = ssh_string;
  clip_ssh.select();
  document.execCommand("copy");
  document.body.removeChild(clip_ssh);
};

function new_exp_copyclipboard_scp(str) {
  function listener(e) {
    e.clipboardData.setData("text/html", str);
    e.clipboardData.setData("text/plain", str);
    e.preventDefault();
  }
  // username@hostname/home/username/path/5db6ffb4495575f385b70150
  // scp -r your_username@hostname:/path . 
  var host = str.substr(0, str.indexOf('/'))
  var path = str.substring(str.indexOf('/')+1)
  var scp_string = "scp -r " + host + ":" + path + "."
  console.log("scp_string is: ", scp_string)
  var clip_scp = document.createElement("input")
  document.body.appendChild(clip_scp);
  clip_scp.setAttribute("id", "clip_scp_id");
  document.getElementById("clip_scp_id").value = scp_string;
  clip_scp.select();
  document.execCommand("copy");
  document.body.removeChild(clip_scp);
};

function new_exp_copyclipboard_sftp(str) {
  function listener(e) {
    e.clipboardData.setData("text/html", str);
    e.clipboardData.setData("text/plain", str);
    e.preventDefault();
  }
  // username@hostname/home/username/path/?username?/5db6ffb4495575f385b70150
  // sftp username@hostname:path/?username?/5db6ce03495575f385b70125/ 
  var host = str.substr(0, str.indexOf('/'))
  var path = str.substring(str.indexOf('/')+1)
  var user = str.substr(0, str.indexOf('@'))+"/"
  var sftp_path = path.slice(path.indexOf(user) + user.length)
  var sftp_string = "sftp " + host + ":" + sftp_path
  console.log("sftp_string is: ", sftp_string)
  var clip_sftp = document.createElement("input")
  document.body.appendChild(clip_sftp);
  clip_sftp.setAttribute("id", "clip_sftp_id");
  document.getElementById("clip_sftp_id").value = sftp_string;
  clip_sftp.select();
  document.execCommand("copy");
  document.body.removeChild(clip_sftp);
};

function new_exp_copyclipboard_justpath(str) {
  function listener(e) {
    e.clipboardData.setData("text/html", str);
    e.clipboardData.setData("text/plain", str);
    e.preventDefault();
  }
  console.log("path is: ", str)
  document.addEventListener("copy", listener);
  document.execCommand("copy");
  document.removeEventListener("copy", listener);
};