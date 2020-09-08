from sqlalchemy import Column, String, Date, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db, BangCap, BoPhan, ChucVu, LoaiDocGia, TinhTrang, TheLoaiSach, LyDoThanhLy


class NhanVien(db.Model, UserMixin):
    __tablename__ = "nhanvien"
    taiKhoan = Column(String(50), primary_key=True)
    matKhau = Column(String(50), nullable=False)
    hoVaTen = Column(String(50), nullable=False)
    sinhNhat = Column(Date, nullable=True)
    diaChi = Column(String(100), nullable=True)
    soDienThoai = Column(String(50), nullable=False)
    bangCap = Column(Enum(BangCap), nullable=False)
    boPhan = Column(Enum(BoPhan), nullable=False)
    chucVu = Column(Enum(ChucVu), nullable=False)
    theDocGia = relationship("TheDocGia", backref="nhanvien", lazy=True)
    thongTinSach = relationship("ThongTinSach", backref="nhanvien", lazy=True)
    phieumuonSach = relationship("PhieuMuonSach", backref="nhanvien", lazy=True)
    phieuThuTienPHat = relationship("PhieuThuTienPhat", backref="nhanvien", lazy=True)
    ghiNhanMatSach = relationship("GhiNhanMatSach", backref="nhanvien", lazy=True)
    thanhLySach = relationship("ThanhLySach", backref="nhanvien", lazy=True)

    def __str__(self):
        return self.hoVaTen

    def get_id(self):
        return self.taiKhoan


class TheDocGia(db.Model):
    __tablename__ = "thedocgia"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoVaTen = Column(String(50), nullable=False)
    loaiDocGia = Column(Enum(LoaiDocGia), nullable=False)
    sinhNhat = Column(Date, nullable=False)
    diaChi = Column(String(100), nullable=True)
    email = Column(String(50), nullable=False, unique=True)
    soLuongSach = Column(Integer, nullable=False, default=0)
    tongNo = Column(Integer, nullable=False, default=0)
    ngayLapThe = Column(Date, nullable=False)
    nguoiLap = Column(String(50), ForeignKey(NhanVien.taiKhoan), nullable=False)
    phieuMuonSach = relationship("PhieuMuonSach", backref="thedocgia", lazy=True)
    phieuThuTienPhat = relationship("PhieuThuTienPhat", backref="thedocgia", lazy=True)
    ghiNhanMatSach = relationship("GhiNhanMatSach", backref="thedocgia", lazy=True)

    def __str__(self):
        return self.id.__str__()


class ThongTinSach(db.Model):
    __tablename__ = "ThongTinSach"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenSach = Column(String(50), nullable=False)
    theLoai = Column(Enum(TheLoaiSach), nullable=False)
    tacGia = Column(String(50), nullable=False)
    namXuatBan = Column(String(50), nullable=False)
    nhaXuatBan = Column(String(50), nullable=False)
    ngayNhap = Column(Date, nullable=False)
    triGia = Column(Integer, nullable=False)
    tinhTrangSach = Column(Enum(TinhTrang), nullable=False)
    theDocGia = Column(Integer, nullable=False)
    nguoiTiepNhan = Column(String(50), ForeignKey(NhanVien.taiKhoan), nullable=False)
    phieuMuonSach = relationship("PhieuMuonSach", backref="thongtinsach", lazy=True)
    ghiNhanMatSach = relationship("GhiNhanMatSach", backref="thongtinsach", lazy=True)

    def __str__(self):
        return self.tenSach


class PhieuMuonSach(db.Model):
    __tablename__ = "PhieuMuonSach"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayMuon = Column(Date, nullable=False)
    docGia = Column(Integer, ForeignKey(TheDocGia.id), nullable=False)
    maSach = Column(Integer, ForeignKey(ThongTinSach.id), nullable=False)
    nguoiTiepNhan = Column(String(50), ForeignKey(NhanVien.taiKhoan), nullable=False)
    phieuTraSach = relationship("PhieuTraSach", backref="phieumuonsach", lazy=True)

    def __str__(self):
        return self.id.__str__()


class PhieuTraSach(db.Model):
    __tablename__ = "PhieuTraSach"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayTra = Column(Date, nullable=False)
    tienPhatKiNay = Column(Integer, nullable=False, default=0)
    tienNo = Column(Integer, nullable=False, default=0)
    tongNo = Column(Integer, nullable=False, default=0)
    phieuMuonSach = Column(Integer, ForeignKey(PhieuMuonSach.id), nullable=False)

    def __str__(self):
        phieuMuonSach = PhieuMuonSach.query.filter_by(id=self.phieuMuonSach).first()
        tenDocGia = TheDocGia.query.filter_by(id=phieuMuonSach.docGia).first()
        return tenDocGia.hoVaTen


class PhieuThuTienPhat(db.Model):
    __tablename__ = "PhieuThuTienPhat"
    id = Column(Integer, primary_key=True, autoincrement=True)
    soTienNo = Column(Integer, nullable=False)
    soTienThu = Column(Integer, nullable=False)
    conLai = Column(Integer, nullable=False)
    nguoiThuTien = Column(String(50), ForeignKey(NhanVien.taiKhoan), nullable=False)
    theDocGia = Column(Integer, ForeignKey(TheDocGia.id), nullable=False)


class GhiNhanMatSach(db.Model):
    __tablename__ = "GhiNhanMatSach"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayGhiNhan = Column(Date, nullable=False)
    tienPhat = Column(Integer, nullable=False, default=0)
    tenSach = Column(Integer, ForeignKey(ThongTinSach.id), nullable=False)
    tenDocGia = Column(Integer, ForeignKey(TheDocGia.id), nullable=False)
    nguoiGhiNhan = Column(String(50), ForeignKey(NhanVien.taiKhoan), nullable=False)


class ThanhLySach(db.Model):
    __tablename__ = "ThanhLySach"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayThanhLy = Column(Date, nullable=False)
    nguoiThanhLy = Column(String(50), ForeignKey(NhanVien.taiKhoan), nullable=False)
    maSach = Column(Integer, nullable=False, default=0)
    tenSach = Column(String(50), nullable=False, default="")
    lyDoThanhLy = Column(Enum(LyDoThanhLy), nullable=False)


if __name__ == ("__main__"):
    db.create_all()
