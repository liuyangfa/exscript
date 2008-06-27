# Copyright (C) 2007 Samuel Abels, http://debain.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
from SpiffWorkQueue import Action

True  = 1
False = 0

class Command(Action):
    def __init__(self, command, wait = True):
        assert command is not None
        Action.__init__(self)
        self.command = command
        self.wait    = wait


    def _on_data_received(self, data, *args):
        self.signal_emit('data_received', data)


    def execute(self, global_lock, global_data, local_data):
        assert global_lock is not None
        assert global_data is not None
        assert local_data  is not None
        local_data['transport'].set_on_data_received_cb(self._on_data_received)
        if self.wait:
            local_data['transport'].execute(self.command)
        else:
            local_data['transport'].send(self.command + '\r')
        local_data['transport'].set_on_data_received_cb(None)
        return True