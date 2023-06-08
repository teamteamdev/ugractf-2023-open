import asyncio
import hashlib
import inspect
from kyzylborda_lib.secrets import get_flag, validate_token
from kyzylborda_lib.server import tcp
import random
import secrets


SOFTWARE = {
    "brute-password": {
        "help": "Crack the password of an account using brute force",
        "args": " <login>",
        "cost": 200
    },
    "cover-tracks": {
        "help": "Confuse forensics systems, enabling safe uninterruptable connection",
        "args": "",
        "cost": 1400
    },
    "inject-code": {
        "help": "Upload a program to server and execute it",
        "args": " <file>",
        "cost": 2000
    },
    "generate-malware": {
        "help": "Generate brand new malware",
        "args": "",
        "cost": 2000
    },
    "brute-tcp": {
        "help": "Use the botnet to send tons of requests to target server",
        "args": " <ip>",
        "cost": 1000
    }
}


GRADES = [
    "Beginner",
    "Intermediate",
    "Expert",
    "Guru",
    "HACKERMAN"
]


JOB_DESCRIPTIONS = {
    "steal_iss": {
        "short": "Steal files from a secure server",
        "long":
            "Hack into the \x1b[32madmin\x1b[0m account at \x1b[32m{iss_ip}\x1b[0m.\n"
            "\x1b[1mDownload\x1b[0m file named \x1b[32m{file_name}\x1b[0m and submit it via \x1b[32mDeepend Bulletin Board\x1b[0m.\n"
    },
    "delete_iss": {
        "short": "Purge information from an internal system",
        "long":
            "Hack into the \x1b[32madmin\x1b[0m account at \x1b[32m{iss_ip}\x1b[0m.\n"
            "\x1b[1mDelete\x1b[0m file named \x1b[32m{file_name}\x1b[0m and get back to us via \x1b[32mDeepend Bulletin Board\x1b[0m.\n"
    },
    "infect_iss": {
        "short": "Infect our rival's server with malware",
        "long":
            "Hack into the \x1b[32madmin\x1b[0m account at \x1b[32m{iss_ip}\x1b[0m.\n"
            "Install a backdoor and provide credentials to us via \x1b[32mDeepend Bulletin Board\x1b[0m.\n"
    },
    "dos_iss": {
        "short": "Crash our competitor's performance",
        "long":
            "Infect any machines of your choice with backdoors and use this botnet to DoS\n"
            "our competitor at \x1b[32m{iss_ip}\x1b[0m.  Once its performance falls to 10 rps,\n"
            "ping us at \x1b[32mDeepend Bulletin Board\x1b[0m.\n"
    }
}


COMPANY_NAMES = [
    "Flylinez",
    "Worthy",
    "Kraftify",
    "Stratechco",
    "RebelRetail",
    "Popn",
    "MavenTek",
    "Edgemark",
    "Catherine",
    "BakerCreek",
    "AllianceArcade",
    "OrbitLink",
    "Piecex",
    "Bizpulse",
    "Birchwood",
    "Inovar",
    "Omnitech",
    "SpireMint",
    "Koncept",
    "CasaSphere",
    "Findnix",
    "CrispForward",
    "Evivo",
    "SkywayVentures",
    "Devotive",
    "SerenityCorp",
    "Exevo",
    "SmartVentures",
    "Techniflex",
    "ZenithusBiz",
    "Rydex",
    "Ictin",
    "ProfitWave",
    "Ikus",
    "Comprite",
    "Logisty",
    "MagnifyNation",
    "KrakenInc",
    "AtlasGroup",
    "AzureVentures",
    "Weal",
    "Cuir",
    "Stratifyr",
    "Zarzo",
    "TopTier",
    "Reveil",
    "SummitNexus",
    "AShape",
    "Orbitrax",
    "Dynamitex",
    "Isation",
    "LinkInnovations",
    "Spectrus",
    "Kalon",
    "Empirea",
    "ThriveCo",
    "Stratonic",
    "SilkWay",
    "DreamSparkz",
    "OverviewIndustries",
    "AdventureWorks",
    "UniteAid",
    "Avatura",
    "Turkfy",
    "Menublaze",
    "Marketsuite",
    "Grouptimez",
    "ClearviewStudios",
    "Gusteo",
    "Genivit",
    "GoBright",
    "Isoni",
    "NextwaveVentures",
    "Coopia",
    "DeviceLink",
    "Kalla",
    "Fleck",
    "CrowdComet",
    "Discombo",
    "Yellivor",
    "Xe",
    "Ayam",
    "Advanse",
    "Othingst",
    "Ropesky",
    "BurgundyBay",
    "Alterno",
    "Mastov",
    "StoreMingle",
    "BeaconVentures",
    "BetterwayBiz",
    "Zenithi",
    "ClickSys",
    "Coretex",
    "Systro",
    "Vitaleeve",
    "Whim",
    "ChordWorx",
    "Profixx",
    "Equinox"
]


class Game:
    def __init__(self, conn: tcp.Connection, token: str):
        self.conn = conn
        self.token = token

        self.current_connection = []
        self.tracks_covered = False
        self.iss_authorized = False

        self.known_hosts = {"10.0.0.13"}
        self.host_names = {
            "10.0.0.13": "Deepend Bulletin Board"
        }
        self.installed_software = set()
        self.local_files = set()

        self.internal_services_systems = {}
        for i, name in enumerate(COMPANY_NAMES):
            self.generate_iss(i, name)
        self.insecure_iss_list = [ip for ip, iss in self.internal_services_systems.items() if not iss["secure"]]
        self.secure_iss_list = [ip for ip, iss in self.internal_services_systems.items() if iss["secure"]]
        self.iss_list = list(self.internal_services_systems)

        self.infected_machines = 0

        # self.banks = {}
        # self.generate_bank("10.0.0.17", "Deepend")
        # self.player_bank_account_id = min(self.banks["10.0.0.17"])
        # self.banks["10.0.0.17"][self.player_bank_account_id]["balance"] = 1000
        # self.store_bank_account_id = max(self.banks["10.0.0.17"])
        self.account_balance = 1000

        self.available_jobs = []
        self.current_job = None
        self.profit = 0
        self.job_iterator = 0
        self.abandoned_jobs = 0
        for _ in range(20):
            self.available_jobs.append(self.generate_job())

        self.secret = secrets.token_bytes(16)


    def generate_iss(self, seed: int, name: str):
        ip = ".".join(map(str, secrets.token_bytes(4)))
        self.internal_services_systems[ip] = {
            "name": name,
            "files": set(),
            "secure": random.randint(0, 2) == 0,
            "infected": False,
            "min_rps": 200
        }
        for i in range(20):
            file_rng = secrets.token_bytes(8)
            file_name = (
                name[:3].upper()
                + "-"
                + file_rng[:3].hex()
                + "-"
                + str(int.from_bytes(file_rng[3:], "little") % 1000000).rjust(6, "0")
            )
            self.internal_services_systems[ip]["files"].add(file_name)
        self.host_names[ip] = f"{name} Internal Services System"


    # def generate_bank(self, ip: str, name: str):
    #     self.banks[ip] = {}
    #     for i in range(20):
    #         rng = hashlib.sha256(f"{ip}/account{i}".encode()).digest()
    #         account_id = str(int.from_bytes(rng[:5], "little") % 1000000).rjust(6, "0")
    #         password = rng[5:9].hex()
    #         balance = int(2 ** (rng[9] / 15))
    #         self.banks[ip][account_id] = {
    #             "password": password,
    #             "balance": balance
    #         }
    #         self.host_names[ip] = f"{name} International Bank"

    # def transfer_funds(
    #     self,
    #     source_bank_ip: str,
    #     source_account_id: str,
    #     target_bank_ip: str,
    #     target_account_id: str,
    #     value: int
    # ) -> str:
    #     source_account = self.banks[source_bank_ip][source_account_id]
    #     if target_bank_ip not in self.banks:
    #         return "Target IP does not resolve to a bank."
    #     if target_account_id not in self.banks[target_bank_ip]:
    #         return "Target bank does not acknowledge the existence of target account."
    #     target_account = self.banks[target_bank_ip][target_account_id]
    #     if value > source_account["balance"]:
    #         return "Insufficient funds."
    #     source_account["balance"] -= value
    #     target_account["balance"] += value
    #     return ""


    def generate_job(self) -> dict:
        rng = hashlib.sha256(f"jobs/{self.job_iterator}".encode()).digest()
        self.job_iterator += 1

        job_level = min(3, rng[0] % (max(0, self.profit) // 10000 + 1))
        if job_level <= 1:
            # Beginner/intermediate
            iss_list = [self.insecure_iss_list, self.secure_iss_list][job_level]
            iss_id = int.from_bytes(rng[1:5], "little") % len(iss_list)
            iss_ip = iss_list[iss_id]
            iss = self.internal_services_systems[iss_ip]

            if iss["files"]:
                file_id = int.from_bytes(rng[5:9], "little") % len(iss["files"])
                file_name = list(iss["files"])[file_id]
            else:
                file_name = (
                    iss["name"][:3].upper()
                    + "-"
                    + rng[5:8].hex()
                    + "-"
                    + str(int.from_bytes(rng[8:13], "little") % 1000000).rjust(6, "0")
                )
                iss["files"].add(file_name)
            return {
                "class": "steal_iss" if rng[9] % 2 == 0 else "delete_iss",
                "iss_ip": iss_ip,
                "file_name": file_name,
                "reward": (rng[13] % 3 + 3) * 100 + 300 * job_level
            }
        elif job_level == 2:
            # Expert
            iss_id = int.from_bytes(rng[1:5], "little") % len(self.iss_list)
            iss_ip = self.iss_list[iss_id]
            return {
                "class": "infect_iss",
                "iss_ip": iss_ip,
                "reward": (rng[5] % 4 + 10) * 100
            }
        elif job_level == 3:
            # Guru
            iss_id = int.from_bytes(rng[1:5], "little") % len(self.iss_list)
            iss_ip = self.iss_list[iss_id]
            return {
                "class": "dos_iss",
                "iss_ip": iss_ip,
                "reward": (rng[5] % 6 + 15) * 100
            }


    async def prompt_command(self) -> str:
        if not self.current_connection:
            await self.conn.writeall("\x1b[36m\x1b[1mlocalhost❯\x1b[0m ".encode())
        else:
            await self.conn.writeall(
                ("\x1b[34m\x1b[1m" + " → ".join(self.current_connection) + "❯\x1b[0m ").encode()
            )
        return (await self.conn.readline()).decode(errors="ignore").strip()

    async def iterate_commands(self, state: str, preprompt: bytes=b""):
        while True:
            self.conn.write(preprompt)
            prompt = await self.prompt_command()
            if prompt:
                cmd = prompt.split()[0].replace("_", "-")
                if cmd == "exit":
                    self.conn.write(b"\n")
                    break
                attr_cmd = cmd.replace("-", "_")
                if cmd in SOFTWARE:
                    fn = getattr(self, f"software__{attr_cmd}", None)
                else:
                    fn = getattr(self, f"{state}__{attr_cmd}", None)
                if fn and (cmd not in SOFTWARE or cmd in self.installed_software):
                    n_params = len(inspect.signature(fn).parameters)
                    args = prompt.split(None, n_params)[1:]
                    if len(args) < n_params:
                        self.conn.write(f"Too few arguments passed to command {cmd}\n\n".encode())
                    else:
                        await fn(*args)
                else:
                    self.conn.write(f"Unknown command {cmd}\n\n".encode())


    async def connect(self, ip: str):
        self.current_connection.append(ip)
        if ip == "10.0.0.13":
            await self.deepend_bulletin_board()
        # elif ip in self.banks:
        #     await self.bank()
        elif ip in self.internal_services_systems:
            await self.iss()
        else:
            self.conn.write(b"\x1b[31mUnresolved IP.\n\x1b[0m\n")
        self.current_connection.pop()


    async def list_installed_software(self):
        for name in self.installed_software:
            self.conn.write(
                ("\x1b[31m⚒ " + (name + "\x1b[0m" + SOFTWARE[name]["args"]).ljust(29) + " " + SOFTWARE[name]["help"] + "\n").encode()
            )


    async def localhost(self):
        self.conn.write(
            "\x1b[36m"
            "Welcome to Deepend, a training simulator for professional hackers!  You're\n"
            "gifted a bank account with a starting balance of $1000.  We don't really care\n"
            "about what you do, but we expect you to get $200000 before your house gets\n"
            "raided by three-letter agencies.  Have fun while you still can!\n"
            "\x1b[0m\n".encode()
        )
        await self.iterate_commands("localhost")

    async def localhost__help(self):
        self.conn.write(
            "\x1b[32m  help\x1b[0m                      Show this help\n"
            "\x1b[32m  ssh\x1b[0m <ip>                  Connect to a server by IP\n"
            "\x1b[32m  hosts\x1b[0m                     Show known hosts\n"
            "\x1b[32m  ls\x1b[0m                        List stored files\n"
            "\x1b[32m  funds\x1b[0m                     Show bank account information\n"
            "\x1b[32m  exit\x1b[0m                      Disconnect\n".encode()
        )
        await self.list_installed_software()
        self.conn.write(b"\n")

    async def localhost__ssh(self, ip: str):
        await self.connect(ip)

    async def localhost__hosts(self):
        current_job_ips = set()
        if self.current_job:
            for attr, value in self.current_job.items():
                if attr.endswith("_ip"):
                    current_job_ips.add(value)

        for ip in sorted(self.known_hosts, key=lambda ip: tuple(map(int, ip.split(".")))):
            if ip in current_job_ips:
                marker = "🌟"
                color = 33
            elif self.host_names[ip].startswith("Deepend "):
                marker = "🏠"
                color = 35
            else:
                marker = "  "
                color = 32
            self.conn.write(
                (f"{marker} \x1b[{color}m" + ip.ljust(15) + "\x1b[0m " + self.host_names[ip] + "\n").encode()
            )
        self.conn.write(b"\n")

    async def localhost__ls(self):
        self.conn.write(f"{len(self.local_files)} file(s) stored\n".encode())
        for file in sorted(self.local_files):
            self.conn.write(f"- \x1b[32m{file}\x1b[0m\n".encode())
        self.conn.write(b"\n")

    async def localhost__funds(self):
        self.conn.write(f"Your balance: $\x1b[34m{self.account_balance}\x1b[0m.\n\n".encode())


    async def deepend_bulletin_board(self):
        self.conn.write(
            "\x1b[1m"
            "┌──────────────────────────────────────────────────────────────────────────────┐\n"
            "│                                                                              │\n"
            "│                                                                              │\n"
            "│                           DEEPEND  BULLETIN  BOARD                           │\n"
            "│                            ░░░░░░░░░░░░░░░░░░░░░░░░                          │\n"
            "│                                                                              │\n"
            "└──────────────────────────────────────────────────────────────────────────────┘\n"
            "\n"
            "Welcome to the first (and only) bulletin board for professional hackers!  Here,\n"
            "you can buy software, get jobs, and measure your progress.\n"
            "\x1b[0m\n".encode()
        )
        await self.iterate_commands(
            "deepend_bulletin_board",
            "Choose option:\n"
            "- \x1b[32msoftware\x1b[0m             List available software\n"
            "- \x1b[32mbuy-software\x1b[0m <name>  Install software\n"
            "- \x1b[32mjobs\x1b[0m                 List jobs\n"
            "- \x1b[32mapply-job\x1b[0m <number>   Apply at jobs\n"
            "- \x1b[32mcurrent-job\x1b[0m          Show information about currently taken job\n"
            "- \x1b[32mabandon-job\x1b[0m          Abandon currently taken job\n"
            "- \x1b[32msubmit-job\x1b[0m           Report job completeness\n"
            "- \x1b[32mexit\x1b[0m                 Disconnect from server\n".encode()
        )

    async def deepend_bulletin_board__software(self):
        for name, info in SOFTWARE.items():
            self.conn.write(
                (
                    f"- \x1b[31m{name}\x1b[0m" +
                    (" [installed]" if name in self.installed_software else "") + "\n"
                    "  " + info["help"] + "\n"
                    "  Cost: $" + str(info["cost"]) + "\n"
                ).encode()
            )
        self.conn.write(b"\n")

    async def deepend_bulletin_board__buy_software(self, name: str):
        if name not in SOFTWARE:
            self.conn.write(b"\x1b[31mDeepend does not sell this software.\n\x1b[0m\n")
            return

        if name in self.installed_software:
            self.conn.write(b"\x1b[31mYou have already bought this program.\n\x1b[0m\n")
            return

        if self.account_balance < SOFTWARE[name]["cost"]:
            self.conn.write(f"\x1b[31mError during SWIFT transaction: Insufficient funds.\n\x1b[0m\n".encode())
            return
        self.account_balance -= SOFTWARE[name]["cost"]
        # err = self.transfer_funds(
        #     "10.0.0.17", self.player_bank_account_id,
        #     "10.0.0.17", self.store_bank_account_id,
        #     SOFTWARE[name]["cost"]
        # )
        # if err:
        #     self.conn.write(f"\x1b[31mError during SWIFT transaction: {err}\n\x1b[0m\n".encode())
        #     return

        self.installed_software.add(name)
        self.conn.write(
            (
                "\x1b[32m"
                "Thank you for buying this software!  You can now use it at any server by using\n"
                "\x1b[1m" + name + "\x1b[0m\x1b[32m as a command name.\n"
                "\x1b[0m\n"
            ).encode()
        )

    async def deepend_bulletin_board__jobs(self):
        self.conn.write(
            b"Short descriptions of available jobs follow.  More information will be\n"
            b"available once you apply.\n"
        )
        for i, job in enumerate(self.available_jobs):
            self.conn.write(
                (
                    f"[#\x1b[32m{i + 1:02}\x1b[0m | $\x1b[34m{job['reward']:5}\x1b[0m] " + JOB_DESCRIPTIONS[job["class"]]["short"] + "\n"
                ).encode()
            )
        self.conn.write(b"\n")

    async def deepend_bulletin_board__apply_job(self, number: str):
        if number.isdigit() and len(number) <= 6 and 1 <= int(number) <= len(self.available_jobs):
            job_number = int(number)
        else:
            self.conn.write(b"\x1b[31mThis job does not exist.\n\x1b[0m\n")
            return

        if self.current_job:
            self.conn.write(
                b"\x1b[31mYou are already on a job and cannot apply for another one.  To abandon the\n"
                b"current job and apply for this one, use \x1b[1mabandon-job\x1b[0m\x1b[31m.  This will\n"
                b"make you lose your grade!\n\x1b[0m\n"
            )
            return

        self.current_job = self.available_jobs[job_number - 1]
        self.available_jobs[job_number - 1] = self.generate_job()
        for attr, value in self.current_job.items():
            if attr.endswith("_ip"):
                self.known_hosts.add(value)

        await self.show_current_job()

    async def deepend_bulletin_board__current_job(self):
        await self.show_current_job()

    async def deepend_bulletin_board__abandon_job(self):
        if not self.current_job:
            self.conn.write(b"\x1b[31mYou are not on a job already.\n\x1b[0m\n")
            return

        self.current_job = None
        self.profit -= 5000
        self.abandoned_jobs += 1

        self.conn.write(
            b"You have abandoned this job.  The customer was not pleased and asked us not to\n"
            b"provide you with further jobs for them.  We have decided that downgrading your\n"
            b"would be of help to other customers as well.\n\n"
        )

        if self.abandoned_jobs == 5:
            await self.conn.writeall(
                b"We are sorry to notify that we are displeased with your work and no longer\n"
                b"desire to employ your services.\n"
            )
            self.conn.close()

    async def deepend_bulletin_board__submit_job(self):
        if not self.current_job:
            self.conn.write(b"\x1b[31mYou are not on a job.\n\x1b[0m\n")
            return

        if self.current_job["class"] == "steal_iss":
            file_name = self.current_job["file_name"]
            if file_name not in self.local_files:
                self.conn.write(
                    "\x1b[31m"
                    f"We have not found a file called \x1b[1m{file_name}\x1b[0m\x1b[31m on your gateway.\n"
                    "Download it from the server before resubmitting.\n"
                    "\x1b[0m\n".encode()
                )
                return
        elif self.current_job["class"] == "delete_iss":
            ip = self.current_job["iss_ip"]
            file_name = self.current_job["file_name"]
            if file_name in self.internal_services_systems[ip]["files"]:
                self.conn.write(
                    "\x1b[31m"
                    f"The employer has informed us they believe you have not removed the file called \x1b[1m{file_name}\x1b[0m\x1b[31m from the server.\n"
                    "Delete it from the server before resubmitting.\n"
                    "\x1b[0m\n".encode()
                )
                return
        elif self.current_job["class"] == "infect_iss":
            ip = self.current_job["iss_ip"]
            iss = self.internal_services_systems[ip]
            if not iss["infected"]:
                self.conn.write(
                    "\x1b[31m"
                    "Backdoor credentials don't work, most likely because malware was not installed.\n"
                    "\x1b[0m\n".encode()
                )
                return
        elif self.current_job["class"] == "dos_iss":
            ip = self.current_job["iss_ip"]
            iss = self.internal_services_systems[ip]
            if iss["min_rps"] > 10:
                self.conn.write(
                    "\x1b[31m"
                    "According to your employer, the service performance has not fallen below 10 rps\n"
                    "recently.\n"
                    "\x1b[0m\n".encode()
                )
                return
        else:
            assert False

        # self.banks["10.0.0.17"][self.player_bank_account_id]["balance"] += self.current_job["reward"]
        self.account_balance += self.current_job["reward"]
        self.profit += self.current_job["reward"]
        self.current_job = None

        self.conn.write(
            b"\x1b[32m"
            b"The employer has confirmed you have completed the task.  Payment has been\n"
            b"delivered to your bank account.\n"
            b"\x1b[0m\n"
        )

        if self.account_balance >= 200000:
            await self.conn.writeall(f"YOUR FLAG: {get_flag(self.token)}\n".encode())
            self.conn.close()

    async def show_current_job(self):
        if not self.current_job:
            self.conn.write(
                b"You are not on a job at the moment.  Feel free to get one at \x1b[32mjobs\x1b[0m.\n\n"
            )
            return

        self.conn.write(
            (
                "Your current job is:\n"
                "| " + JOB_DESCRIPTIONS[self.current_job["class"]]["long"].format(**self.current_job).replace("\n", "\n| ") +
                f"Reward: $\x1b[34m{self.current_job['reward']}\x1b[0m\n"
                "\n"
            ).encode()
        )


    # async def bank(self):
    #     ip = self.current_connection[-1]
    #     self.conn.write(
    #         (
    #             "\x1b[1mWelcome to " + self.host_names[ip] + "!\n"
    #             "\x1b[0m\n"
    #         ).encode()
    #     )
    #     await self.iterate_commands("bank")

    async def iss(self):
        ip = self.current_connection[-1]
        self.conn.write(
            (
                "\x1b[1m"
                "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
                "@                                                                              @\n"
                "@ " + self.host_names[ip].ljust(76) + " @\n"
                "@                                                                              @\n"
                "@ UNAUTHORIZED ACCESS FORBIDDEN                                                @\n"
                "@                                                                              @\n"
                "@ LOGIN NOW                                                                    @\n"
                "@                                                                              @\n"
                "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
                "\n"
                "\x1b[0m\n"
            ).encode()
        )
        await self.iterate_commands("iss")

    async def iss__help(self):
        self.conn.write(
            "\x1b[32m  help\x1b[0m                      Show this help\n"
            "\x1b[32m  login\x1b[0m <login> <password>  Authorize\n"
            "\x1b[32m  exit\x1b[0m                      Disconnect\n".encode()
        )
        await self.list_installed_software()
        self.conn.write(b"\n")

    async def iss__login(self, login: str, password: str):
        if login != "admin":
            self.conn.write(b"\x1b[31mInvalid username.\n\x1b[0m\n")
            return

        ip = self.current_connection[-1]
        rng = hashlib.sha256(f"iss-ip/{ip}/".encode() + self.secret).digest()
        if password != rng[:4].hex():
            self.conn.write(b"\x1b[31mWrong password.\n\x1b[0m\n")
            return

        await self.iss_auth()

    async def iss_auth(self):
        self.conn.write(
            b"\x1b[32mYou are now authorized as \x1b[1madmin\x1b[0m\x1b[32m.\n"
            b"\n"
        )
        self.iss_authorized = True
        await self.iterate_commands("iss_auth")
        self.iss_authorized = False

    async def iss_auth__help(self):
        self.conn.write(
            "\x1b[32m  help\x1b[0m                      Show this help\n"
            "\x1b[32m  ls\x1b[0m                        List available files\n"
            "\x1b[32m  rm\x1b[0m <file>                 Delete file\n"
            "\x1b[32m  download\x1b[0m <file>           Download file to local PC\n"
            "\x1b[32m  exit\x1b[0m                      Logout\n".encode()
        )
        await self.list_installed_software()
        self.conn.write(b"\n")

    async def iss_auth__ls(self):
        ip = self.current_connection[-1]
        iss = self.internal_services_systems[ip]
        self.conn.write(f"{len(iss['files'])} file(s) stored\n".encode())
        for file in sorted(iss["files"]):
            self.conn.write(f"- \x1b[32m{file}\x1b[0m\n".encode())
        self.conn.write(b"\n")

    async def iss_auth__rm(self, file: str):
        ip = self.current_connection[-1]
        iss = self.internal_services_systems[ip]
        if file in iss["files"]:
            iss["files"].remove(file)
            self.conn.write(f"File \x1b[32m{file}\x1b[0m deleted successfully.\n\n".encode())
        else:
            self.conn.write(f"\x1b[31mFile \x1b[1m{file}\x1b[0m\x1b[31m does not exist.\n\x1b[0m\n".encode())

    async def iss_auth__download(self, file: str):
        ip = self.current_connection[-1]
        iss = self.internal_services_systems[ip]
        if file in iss["files"]:
            self.local_files.add(file)
            self.conn.write(f"File \x1b[32m{file}\x1b[0m downloaded successfully.\n\n".encode())
        else:
            self.conn.write(f"\x1b[31mFile \x1b[1m{file}\x1b[0m\x1b[31m does not exist.\n\x1b[0m\n".encode())


    async def software__brute_password(self, login: str):
        if not self.current_connection:
            password = "el1t3_h4xx0r"
        else:
            ip = self.current_connection[-1]
            if ip in self.internal_services_systems:
                if login != "admin":
                    self.conn.write("\x1b[31mInvalid username.\n\x1b[0m\n".encode())
                    return
                iss = self.internal_services_systems[ip]
                if iss["secure"] and not self.tracks_covered:
                    self.conn.write(
                        "\x1b[31m"
                        "This server has forensics systems that confuse brute force.  Install\n"
                        "\x1b[1mcover-tracks\x1b[0m\x1b[31m to circumvent them.\n"
                        "\x1b[0m\n".encode()
                    )
                    return
                rng = hashlib.sha256(f"iss-ip/{ip}/".encode() + self.secret).digest()
                password = rng[:4].hex()
            else:
                self.conn.write("\x1b[31mDon't know how to crack this machine.\n\x1b[0m\n".encode())
                return

        await self.conn.writeall(b"Cracking...\n")
        await asyncio.sleep(0.5)
        self.conn.write(
            f"\x1b[31mThe password is \x1b[1m{password}\x1b[0m\x1b[31m.\n\x1b[0m\n".encode()
        )

    async def software__cover_tracks(self):
        self.tracks_covered = True
        self.conn.write(
            b"All your connections are now protected.  You don't need to run this program"
            b"during any other connections.\n\n"
        )

    async def software__inject_code(self, file: str):
        if file not in self.local_files:
            self.conn.write(f"\x1b[31mFile \x1b[1m{file}\x1b[0m\x1b[31m does not exist.\n\x1b[0m\n".encode())
            return

        if not file.endswith(".exe"):
            self.conn.write(f"\x1b[31mFile \x1b[1m{file}\x1b[0m\x1b[31m is not executable.\n\x1b[0m\n".encode())
            return

        if not self.current_connection:
            self.conn.write(b"\x1b[31mCannot run code on gateway.\n\x1b[0m\n")
            return

        ip = self.current_connection[-1]
        if ip in self.internal_services_systems:
            if not self.iss_authorized:
                self.conn.write(b"\x1b[31mInsufficient permissions on target machine.\n\x1b[0m\n")
                return

            iss = self.internal_services_systems[ip]
            if iss["secure"] and not self.tracks_covered:
                self.conn.write(
                    b"\x1b[31m"
                    b"This server has forensics systems that confuse code injection.  Install\n"
                    b"\x1b[1mcover-tracks\x1b[0m\x1b[31m to circumvent them.\n"
                    b"\x1b[0m\n"
                )
                return

            if file.startswith("backdoor-"):
                if not iss["infected"]:
                    self.infected_machines += 1
                iss["infected"] = True
        else:
            self.conn.write(b"\x1b[31mDon't know how to inject code to this machine.\n\x1b[0m\n")
            return

        self.conn.write(b"Code injected.\n\n")

    async def software__generate_malware(self):
        await self.conn.writeall(b"Generating...\n")
        await asyncio.sleep(0.5)

        backdoor_name = "backdoor-" + secrets.token_bytes(3).hex() + ".exe"
        self.local_files.add(backdoor_name)
        self.conn.write(
            f"Backdoor \x1b[32m{backdoor_name}\x1b[0m generated.\n\n".encode()
        )

    async def software__brute_tcp(self, ip: str):
        if ip not in self.host_names:
            self.conn.write(b"\x1b[31mUnresolved IP.\n\x1b[0m\n")
            return

        await self.conn.writeall(b"DoSing the server...\n")
        for i in range(10):
            rps = int(200 / (1 + self.infected_machines * (1 + i) / 10))
            await asyncio.sleep(0.3)
            await self.conn.writeall(f"The estimated throughput of the server is {rps} rps\n".encode())

        rps = 200 // (1 + self.infected_machines)
        if ip in self.internal_services_systems:
            iss = self.internal_services_systems[ip]
            iss["min_rps"] = min(iss["min_rps"], rps)

        self.conn.write(b"\n")


@tcp.listen
async def handle(conn: tcp.Connection):
    await conn.writeall(b"Token: ")
    token = (await conn.readline()).decode(errors="ignore").strip()
    if not validate_token(token):
        await conn.writeall(b"Invalid token\n")
        return

    game = Game(conn, token)
    await game.localhost()
