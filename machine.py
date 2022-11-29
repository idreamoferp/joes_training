import logging, atexit

class Machine(object):
    def __init__(self, api, asset_id, config):
        #sets an on exit function
        atexit.register(self.quit)
        
        #save the odoo api object sent from the caller to this object for future use.
        self.api = api

        #save the config object sent from the caller to this object for future use.
        self.config = config

        #place holder for the odoo equipment object for future use.
        self.equipment_id = False 
        
        #fetches the odoo equipment object from the maintence module, if it exists, and saves it in the place
        #holder created above. if no object exists in odoo, the equipment id will stay False
        self.equipment_id = self.api.env['maintenance.equipment'].browse(self.config['equipment_id'])
        
        #creates a logger object specific to this peice of equiptment, this help to know where logging entries
        #originate in the log files.
        self._logger = logging.getLogger(self.name or "Machine")
        
        #log that the "machine has initalized."
        self._logger.info("Machine INIT Compleete.")
        return
    
    def get_uom_id(self, uom_name):
        #a helper method to get a unit of measure odoo object from the remote database with the name of 'uom_name'
        domain = [("name", "=", uom_name)]
        uom_id = self.api.env['uom.uom'].search(domain)
        if uom_id:
            uom_id = self.api.env['uom.uom'].browse(uom_id[0])
        return uom_id
    
    @property
    def name(self):
        #fetches the name recorded in odoo maintence system for this equpitment.
        if self.equipment_id:
            return self.equipment_id.name
        return None
            
    def get_blocking_status(self):
        #not yet implemented in odoo, return false to indicate the machine is not blocked from running
        return False
        
    def quit(self):
        #when the application running this class, quits for any reason, run this method to close up any objects
        #that may be in use or stop any threads that need be stopped.
        self._logger.info("Machine Shutdown.")
        pass