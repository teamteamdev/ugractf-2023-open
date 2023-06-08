{
  outputs = { ... }: {
    kyzylModules.default = { instance, ... }: { ... }: {
      networking.firewall = {
        allowedUDPPorts = [
          51820 # ohgodno
        ];
        allowedTCPPorts = [
          5917 # deepend
          6069 # summerspent
	  18602 # repeatafterme
        ];
      };

      services.kyzylborda.instances.${instance}.extraHostnames = [ "uniiiu.mooo.com" ];
    };
  };
}
