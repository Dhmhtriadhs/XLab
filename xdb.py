import os, sqlite3

class xdb:
    """xdb for ."""

    def __init__(self):
        self.conn = sqlite3.connect("xdb.db", check_same_thread=False)

    def close(self):
        self.conn.close()

    def addBodypart(self, en, gr):
        cur = self.conn.cursor()
        cur.execute('insert into bodyparts (en, gr) values (?, ?)', (en, gr))
        self.conn.commit()

    def removeBodypart(self, id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM bodyparts WHERE id=?;', (id, ))
        self.conn.commit()

    def getBodyparts(self):
        cur = self.conn.cursor()
        datas = cur.execute('select id, en, gr from bodyparts;')
        bodyparts = {}
        for data in datas:
            id,en,gr = data
            bodyparts[str(id)] = [en,gr]
        self.conn.commit()
        return bodyparts

    def getExams(self, id):
        cur = self.conn.cursor()
        datas = cur.execute('select id, en, gr, kvfrom, kvto from exams where bodyID=?;',(id,))
        exams = {}
        for data in datas:
            id,en,gr,kvfrom,kvto = data
            exams[str(id)] = [en,gr,kvfrom,kvto]
        self.conn.commit()
        return exams

    def addExam(self, bodyID, en, gr, kvfrom, kvto):
        cur = self.conn.cursor()
        cur.execute('insert into exams (bodyID, en, gr, kvfrom, kvto) values (?,?,?,?,?)', (bodyID, en, gr, kvfrom, kvto))
        self.conn.commit()

    def removeExam(self, id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM exams WHERE id=?;', (id, ))
        cur.execute('DELETE FROM xrays WHERE examID=?;', (id, ))
        self.conn.commit()

    def getXrays(self, examID):
        cur = self.conn.cursor()
        datas = cur.execute('select id, name, realname, patient, kV, mAs, grid, stand, weight, xray_src from xrays where examID=?;',(int(examID),))
        xrays = {}
        for data in datas:
            id, name, realname, patient, kV, mAs, grid, stand, weight, xray_src = data
            xrays[str(id)] = [name, realname, patient, kV, mAs, grid, stand, weight, xray_src]
        self.conn.commit()
        return xrays

    def addXray(self, jsn):
        src = jsn["xsrc"]#.split("/")[-1]
        cur = self.conn.cursor()
        cur.execute('insert into xrays (examID, name, realname, patient, kV, mAs, grid, stand, weight, xray_src) '+
            'values (?,?,?,?,?,?,?,?,?,?)', (jsn["examID"],jsn["xname"],jsn["real"],
            jsn["patient"],jsn["kV"],jsn["mAs"],jsn["grid"],jsn["stand"],
            jsn["weight"],src,))
        self.conn.commit()

    def getPatient(self, id):
        cur = self.conn.cursor()
        data = {}
        patients = cur.execute('select examID, name, patient, kV, mAs, grid, stand, weight, xray_src from xrays where id=?;',(int(id),))
        for patient in patients:
            examID, name, patient, kV, mAs, grid, stand, weight, xray_src= patient
            data = {"examID":examID, "name":name, "patient":patient, "kV":kV,
                "mAs":mAs, "grid":grid, "stand":stand, "weight":weight,
                "xray_src":xray_src}

        self.conn.commit()
        return data

    def getQRs(self):
        cur = self.conn.cursor()
        data = {}
        patients = cur.execute('select id, name from xrays;')
        for patient in patients:
            id, name = patient
            data[str(id)] = name
        self.conn.commit()
        return data

    def removeXray(self, id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM xrays WHERE id=?;', (id, ))
        self.conn.commit()
