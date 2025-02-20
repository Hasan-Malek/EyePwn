# EyePwn

**EyePwn** is a powerful and efficient **IP Camera Brute-Force & Enumeration Tool** designed for cybersecurity professionals and penetration testers. This tool helps in identifying weak or default credentials on IP-based surveillance systems.

![EyePwn](https://github.com/user-attachments/assets/e4a1ba08-34e0-4525-b9c4-1a9daa6cde6e)


## 🚀 Features
- 🔍 **Fast & Asynchronous** brute-force attack with `aiohttp`
- 🔑 **Custom Credential List** support
- 🎯 **Target Multiple IPs** from a file
- 📡 **Auto-Detection of IP Cameras**
- 📜 **Logging of Successful Attempts**
- 🌐 **User-Agent Randomization** for better anonymity
- 🖥️ **Debug Mode** for better analysis

## 📦 Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/EyePwn.git
cd EyePwn

# Install dependencies
pip install -r requirements.txt
```

## 🛠️ Usage
```bash
python3 main.py --help
```

![s1](https://github.com/user-attachments/assets/61514c67-c230-4682-968f-e210198b2672)


### Options:
```bash
  -h, --help            show this help message and exit
  -tf, --targets_file TARGETS_FILE
                        File with target IPs
  -cf, --combo_file COMBO_FILE
                        File with login:password combos
  -lf, --logins_file LOGINS_FILE
                        File with logins
  -pf, --passwords_file PASSWORDS_FILE
                        File with passwords
  -r, --results_file RESULTS_FILE
                        File to store successful attempts
  -t, --threads THREADS
                        Number of parallel connections
  -to, --timeout TIMEOUT
                        Timeout for requests
  -p, --proxy PROXY     SOCKS5 proxy (e.g., socks5://127.0.0.1:9050)
  -glc, --generate_login_combo
                        Generate login:login combos
  -d, --debug           Enable debug output
  --no-camera-check     Skip camera detection and brute-force all targets
```


## 📌 Example
```bash
python3 main.py -tf ip.txt -cf cred.txt --debug
```

![s2](https://github.com/user-attachments/assets/576d3beb-f874-454d-bb38-264d947c0bd6)


## 📜 Sample Files
### **Target IP List (ip.txt)**
```
192.168.1.10
192.168.1.15
182.75.239.162
```

![s3](https://github.com/user-attachments/assets/4df8f7d4-cdb6-448c-8495-30550e7fb0d7)


## 🛡️ Disclaimer
**EyePwn is intended for security research and educational purposes only.** Unauthorized access to systems you do not own is illegal. Use this tool responsibly and only with proper authorization.

## 🏆 Contributing
Pull requests and contributions are welcome! Feel free to open issues for bugs, feature requests, or enhancements.

## 📜 License
This project is licensed under the **MIT License**.

## 🌍 Connect with Me
- **GitHub**: [yourgithub](https://github.com/Hasan-Malek)
- **LinkedIn**: [yourlinkedin](https://www.linkedin.com/in/hasan-malek-125036297/)

---
**Built for ethical hacking, penetration testing, and cybersecurity professionals! 🛡️💻**

