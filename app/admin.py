import hashlib, math
from datetime import date

from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import validators
from flask_login import current_user, logout_user
from flask import redirect, request, session

from app.models import *
from app import admin, dao


class NhanVienView(ModelView):
    column_display_pk = True
    column_exclude_list = ['matKhau']
    column_labels = dict(taiKhoan="Tài khoản", matKhau="Mật khẩu", hoVaTen="Họ và tên", sinhNhat="Sinh nhật",
                         diaChi="Địa chỉ", soDienThoai="Số điện thoại", bangCap="Bằng cấp", boPhan="Bộ phận",
                         chucVu="Chức vụ")
    form_columns = (
        'taiKhoan', 'matKhau', 'hoVaTen', 'sinhNhat', 'diaChi', 'soDienThoai', 'bangCap', 'boPhan',
        'chucVu')
    form_widget_args = {
        'matKhau': {
            'type': 'password'
        }
    }

    def on_model_change(self, form, NhanVien, is_created=False):
        NhanVien.matKhau = hashlib.md5(NhanVien.matKhau.encode('utf-8')).hexdigest()

    def _bangCap_formatter(view, context, model, name):
        if model.bangCap:
            bangcap = model.bangCap.value
            return bangcap
        else:
            return ""

    def _boPhan_formatter(view, context, model, name):
        if model.boPhan:
            boPhan = model.boPhan.value
            return boPhan
        else:
            return ""

    def _chucVu_formatter(view, context, model, name):
        if model.chucVu:
            chucVu = model.chucVu.value
            return chucVu
        else:
            return ""

    column_formatters = {
        'bangCap': _bangCap_formatter,
        'boPhan': _boPhan_formatter,
        'chucVu': _chucVu_formatter
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.boPhan == BoPhan.BanGiamDoc


class TheDocGiaView(ModelView):
    column_display_pk = True
    column_labels = dict(id="Mã thẻ", hoVaTen="Họ và tên", loaiDocGia="Loại độc giả", sinhNhat="Sinh nhật",
                         diaChi="Địa chỉ", ngayLapThe="Ngày lập thẻ", nhanvien="Nhân Viên", soLuongSach="Số lượng sách",
                         tongNo="Tổng nợ")
    column_sortable_list = ['id', 'hoVaTen', 'loaiDocGia', 'sinhNhat', 'diaChi', 'email', 'ngayLapThe',
                            ('nhanvien', ('nhanvien.hoVaTen'))]
    form_excluded_columns = ['ngayLapThe', 'nhanvien', 'phieuMuonSach', 'soLuongSach', 'tongNo', 'ghiNhanMatSach',
                             'phieuThuTienPhat']

    def on_model_change(self, form, TheDocGia, is_created=False):
        TheDocGia.ngayLapThe = str(date.today())
        TheDocGia.nguoiLap = current_user.taiKhoan
        age = math.ceil((date.today() - form.sinhNhat.data).days / 365)

        if age < 18 or age > 55:
            raise validators.ValidationError("Xin lối độ tuổi quý khách không hợp lệ để lập thẻ!")
        else:
            super().on_model_change(form, TheDocGia, is_created)

    def _loaiDocGia_formatter(view, context, model, name):
        if model.loaiDocGia:
            loaidocgia = model.loaiDocGia.value
            return loaidocgia
        else:
            return ""

    column_formatters = {
        'loaiDocGia': _loaiDocGia_formatter
    }

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.boPhan == BoPhan.ThuThu or current_user.boPhan == BoPhan.BanGiamDoc)


class ThongTinSachView(ModelView):
    column_display_pk = True
    column_labels = dict(id="Mã sách", tenSach="Tên sách", theLoai="Thể loại", tacGia="Tác giả",
                         namXuatBan="Năm xuất bản", nhaXuatBan="Nhà xuất bản", ngayNhap="Ngày nhập", triGia="Trị giá",
                         tinhTrangSach="Tình trạng sách", nhanvien="Nhân viên", theDocGia="Thẻ độc giả")
    column_sortable_list = ['id', 'tenSach', 'theLoai', 'tacGia',
                            'namXuatBan', 'nhaXuatBan', 'ngayNhap', 'triGia',
                            'tinhTrangSach', ('nhanvien', ('nhanvien.hoVaTen')), 'theDocGia']
    form_excluded_columns = ['ngayNhap', 'nhanvien', 'tinhTrangSach', 'phieuMuonSach', 'ghiNhanMatSach', 'theDocGia']

    def on_model_change(self, form, ThongTinSach, is_created=False):
        ThongTinSach.ngayNhap = str(date.today())
        ThongTinSach.tinhTrangSach = TinhTrang.Tontai
        ThongTinSach.nguoiTiepNhan = current_user.taiKhoan
        namXuatBanToiThieu = date.today().year - int(ThongTinSach.namXuatBan)

        if namXuatBanToiThieu > 8:
            raise validators.ValidationError("Xin lối năm xuất bản quá thời gian quy định(8 năm)!")

    def _tinhTrangSach_formatter(view, context, model, name):
        if model.tinhTrangSach:
            tinhtrang = model.tinhTrangSach.value
            return tinhtrang
        else:
            return ""

    column_formatters = {
        'tinhTrangSach': _tinhTrangSach_formatter
    }

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.boPhan == BoPhan.ThuKho or current_user.boPhan == BoPhan.BanGiamDoc)


class PhieuMuonSachView(ModelView):
    column_display_pk = True
    column_list = ['id', 'ngayMuon', 'nhanvien', 'thedocgia.hoVaTen', 'thongtinsach']
    column_labels = {'id': "Mã phiếu", 'ngayMuon': "Ngày mượn", 'nhanvien': "Nhân viên",
                     'thedocgia.hoVaTen': "Tên độc giả",
                     'thongtinsach': "Tên sách", 'thedocgia': "Mã thẻ"}
    column_sortable_list = ['id', 'ngayMuon', ('nhanvien', ('nhanvien.hoVaTen')), 'thedocgia.hoVaTen',
                            ('thongtinsach', ('thongtinsach.tenSach'))]
    form_excluded_columns = ['ngayMuon', 'nhanvien', 'phieuTraSach']

    def on_model_change(self, form, PhieuMuonSach, is_created=False):
        PhieuMuonSach.ngayMuon = str(date.today())
        PhieuMuonSach.nguoiTiepNhan = current_user.taiKhoan
        thongTinSach = ThongTinSach.query.get(form.thongtinsach.data.id)
        theDocGia = TheDocGia.query.get(form.thedocgia.data.id)
        ngayHetHan = (date.today() - theDocGia.ngayLapThe).days

        if ngayHetHan > 180:
            raise validators.ValidationError("Xin lối thẻ đã hết hạn!")
        else:
            if thongTinSach.tinhTrangSach == TinhTrang.DangDuocMuon:
                raise validators.ValidationError("Xin lỗi sách hiện đang được mượn!")
            else:
                if thongTinSach.tinhTrangSach == TinhTrang.KhongTonTai or thongTinSach.tinhTrangSach == TinhTrang.DaThanhLy:
                    raise validators.ValidationError("Xin lỗi sách hiện không tồn tại hoặc đã được thanh lý!")
                else:
                    if theDocGia.soLuongSach >= 5:
                        raise validators.ValidationError("Xin lỗi sách mượn đã vượt quá quy định(5cuốn)!")
                    else:
                        thongTinSach.theDocGia = form.thedocgia.data.id
                        thongTinSach.tinhTrangSach = TinhTrang.DangDuocMuon
                        theDocGia.soLuongSach += 1
                        db.session.add(theDocGia, thongTinSach)
                        db.session.commit()
                        super().on_model_change(form, PhieuMuonSach, is_created)

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.boPhan == BoPhan.ThuThu or current_user.boPhan == BoPhan.BanGiamDoc)


class PhieuTraSachView(ModelView):
    column_display_pk = True
    column_list = ["id", "ngayTra", "tienPhatKiNay", "tienNo", "tongNo", "phieumuonsach.thedocgia.hoVaTen",
                   "phieumuonsach.thongtinsach.tenSach"]
    column_labels = {'id': "Mã phiếu", 'ngayTra': "Ngày trả", 'tienPhatKiNay': "Tiền phạt kì này", 'tienNo': "Tiền nợ",
                     'tongNo': "Tổng nợ", 'phieumuonsach.thedocgia.hoVaTen': "Tên độc giả",
                     'phieumuonsach.thongtinsach.tenSach': "Tên sách", 'phieumuonsach': "Phiếu mượn sách"}
    column_sortable_list = ['id', 'ngayTra', 'tienPhatKiNay', 'tienNo',
                            'tongNo', 'phieumuonsach.thedocgia.hoVaTen',
                            'phieumuonsach.thongtinsach.tenSach']
    form_columns = ["phieumuonsach"]

    def on_model_change(self, form, PhieuTraSach, is_created=False):
        tienPhatKiNay = 0
        PhieuTraSach.ngayTra = str(date.today())
        theDocGia = TheDocGia.query.get(form.phieumuonsach.data.docGia)
        thongTinSach = ThongTinSach.query.get(form.phieumuonsach.data.maSach)
        hanTraSach = (date.today() - form.phieumuonsach.data.ngayMuon).days

        if thongTinSach.tinhTrangSach == TinhTrang.Tontai:
            raise validators.ValidationError("Xin lỗi không thể trả sách đã tồn tại!")
        else:
            if thongTinSach.tinhTrangSach == TinhTrang.KhongTonTai or thongTinSach.tinhTrangSach == TinhTrang.DaThanhLy:
                raise validators.ValidationError("Xin lỗi sách hiện không tồn tại hoặc đã được thanh lý!")
            else:
                if form.phieumuonsach.data.docGia != thongTinSach.theDocGia:
                    raise validators.ValidationError("Xin lỗi độc giả hiện không mượn sách này!")
                else:
                    if hanTraSach > 4:
                        tienPhatKiNay = (hanTraSach - 4) * 1000

                    PhieuTraSach.tienPhatKiNay = tienPhatKiNay
                    PhieuTraSach.tienNo = theDocGia.tongNo
                    PhieuTraSach.tongNo = tienPhatKiNay + PhieuTraSach.tienNo

                    theDocGia.soLuongSach -= 1
                    theDocGia.tongNo = PhieuTraSach.tongNo
                    db.session.add(theDocGia)
                    db.session.commit()

                    thongTinSach.tinhTrangSach = TinhTrang.Tontai
                    thongTinSach.theDocGia = 0
                    db.session.add(thongTinSach)
                    db.session.commit()
                    super().on_model_change(form, PhieuTraSach, is_created)

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.boPhan == BoPhan.ThuThu or current_user.boPhan == BoPhan.BanGiamDoc)


class PhieuThuTienPhatView(ModelView):
    column_display_pk = True
    column_list = ['id', 'soTienNo', 'soTienThu', 'conLai', 'thedocgia.hoVaTen', 'nhanvien']
    column_labels = {
        'id': 'Mã Phiếu',
        'soTienNo': 'Tiền nợ',
        'soTienThu': 'Số tiền thu',
        'conLai': 'Còn lại',
        'nhanvien': 'Nhân viên',
        'thedocgia': 'Mã thẻ độc giả',
        'thedocgia.hoVaTen': 'Tên độc giả',
    }
    column_sortable_list = ['id', 'soTienNo', 'soTienThu', 'conLai', ('nhanvien', ('nhanvien.hoVaTen')),
                            'thedocgia.hoVaTen']
    form_excluded_columns = ['conLai', 'soTienNo', 'nhanvien']

    def on_model_change(self, form, PhieuThuTienPhat, is_created=False):
        if form.thedocgia.data.tongNo == 0:
            raise validators.ValidationError("Độc giả không nợ tiền!")
        else:
            if form.soTienThu.data > form.thedocgia.data.tongNo:
                raise validators.ValidationError("Xin lỗi số tiền thu vượt quá số tiền nợ!")
            else:
                if form.soTienThu.data > 0:
                    conLai = form.thedocgia.data.tongNo - form.soTienThu.data
                else:
                    raise validators.ValidationError("Xin lỗi số tiền thu không được nhỏ hơn 0!")

                PhieuThuTienPhat.nguoiThuTien = current_user.taiKhoan
                PhieuThuTienPhat.conLai = conLai
                theDocGia = TheDocGia.query.get(form.thedocgia.data.id)
                PhieuThuTienPhat.soTienNo = theDocGia.tongNo
                theDocGia.tongNo = conLai
                db.session.add(theDocGia)
                db.session.commit()

                super().on_model_change(form, PhieuThuTienPhat, is_created)

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.boPhan == BoPhan.ThuQuy or current_user.boPhan == BoPhan.BanGiamDoc)


class GhiNhanMatSachView(ModelView):
    column_list = ['ngayGhiNhan', 'tienPhat', 'nhanvien', 'thedocgia.hoVaTen', 'thongtinsach.tenSach']
    column_labels = {
        'ngayGhiNhan': "Ngày ghi nhận", 'tienPhat': "Tiền phạt", 'nhanvien': "Nhân viên",
        'thedocgia.hoVaTen': 'Tên độc giả', 'thongtinsach.tenSach': 'Tên sách',
    }
    column_sortable_list = ['ngayGhiNhan', 'tienPhat', ('nhanvien', ('nhanvien.hoVaTen')), 'thedocgia.hoVaTen',
                            'thongtinsach.tenSach']
    form_excluded_columns = ['ngayGhiNhan', 'nhanvien']

    def on_model_change(self, form, GhiNhanMatSach, is_created=False):
        GhiNhanMatSach.ngayGhiNhan = str(date.today())
        GhiNhanMatSach.nguoiGhiNhan = current_user.taiKhoan
        thongTinSach = ThongTinSach.query.get(form.thongtinsach.data.id)
        theDocGia = TheDocGia.query.get(form.thedocgia.data.id)

        if form.tienPhat.data < form.thongtinsach.data.triGia:
            raise validators.ValidationError("Xin lỗi số tiền phạt nhỏ hơn trị giá sách!")
        else:
            if thongTinSach.tinhTrangSach == TinhTrang.Tontai:
                raise validators.ValidationError("Xin lỗi sách đang tồn tại!")
            else:
                if thongTinSach.tinhTrangSach == TinhTrang.KhongTonTai or thongTinSach.tinhTrangSach == TinhTrang.DaThanhLy:
                    raise validators.ValidationError("Xin lỗi sách hiện không tồn tại hoặc đã được thanh lý!")
                else:
                    if form.thedocgia.data.id != form.thongtinsach.data.theDocGia:
                        raise validators.ValidationError("Xin lỗi độc giả không mượn sách này!")
                    else:
                        thongTinSach.tinhTrangSach = TinhTrang.KhongTonTai
                        theDocGia.tongNo += form.tienPhat.data
                        theDocGia.soLuongSach -= 1
                        db.session.add(thongTinSach, theDocGia)
                        db.session.commit()
                        super().on_model_change(form, GhiNhanMatSach, is_created)

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.boPhan == BoPhan.ThuThu or current_user.boPhan == BoPhan.BanGiamDoc)


class ThanhLySachView(ModelView):
    column_labels = {'ngayThanhLy': "Ngày thanh lý", 'maSach': "Mã sách", 'tenSach': "Tên sách",
                     'lyDoThanhLy': "Lý do thanh lý", 'nhanvien': "Nhân viên"}
    column_sortable_list = ['ngayThanhLy', 'maSach', 'tenSach',
                            'lyDoThanhLy', ('nhanvien', ('nhanvien.hoVaTen'))]
    form_excluded_columns = ['ngayThanhLy', 'tenSach', 'nhanvien']

    def _lyDoThanhLy_formatter(view, context, model, name):
        if model.lyDoThanhLy:
            lydothanhly = model.lyDoThanhLy.value
            return lydothanhly
        else:
            return ""

    column_formatters = {
        'lyDoThanhLy': _lyDoThanhLy_formatter
    }

    def on_model_change(self, form, ThanhLySach, is_created=False):
        ThanhLySach.ngayThanhLy = str(date.today())
        ThanhLySach.nguoiThanhLy = current_user.taiKhoan
        thongTinSach = ThongTinSach.query.get(form.maSach.data)

        if thongTinSach == None:
            raise validators.ValidationError("Xin lỗi sách không tồn tại!")
        else:
            ThanhLySach.tenSach = thongTinSach.tenSach
            thongTinSach.tinhTrangSach = TinhTrang.DaThanhLy
            db.session.add(thongTinSach)
            db.session.commit()
            super().on_model_change(form, GhiNhanMatSach, is_created)

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.boPhan == BoPhan.ThuKho or current_user.boPhan == BoPhan.BanGiamDoc)


class ThoatView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


class DanhSachSachView(BaseView):
    @expose('/')
    def __index__(self):
        tenSach = request.args.get("tenSach")
        theLoai = request.args.get("theLoai")
        tacGia = request.args.get("tacGia")
        tinhTrang = request.args.get("tinhTrang")

        return self.render('admin/list.html', books=dao.read_book_infos(tenSach=tenSach, theLoai=theLoai, tacGia=tacGia,
                                                                        tinhTrang=tinhTrang), tinhTrang=TinhTrang,
                           theLoai=TheLoaiSach)


class ThongKeView(BaseView):
    @expose('/')
    def __index__(self):
        thang = request.args.get("thang") or 0
        session['thang'] = thang
        return self.render('admin/summary.html', theLoaiA=len(dao.theLoaiA(thang=thang)),
                           theLoaiB=len(dao.theLoaiB(thang=thang)), theLoaiC=len(dao.theLoaiC(thang=thang)),
                           traTre=dao.sachTraTre(thang=thang), docGia=dao.docGiaNoTien(), date=date.today())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.boPhan == BoPhan.BanGiamDoc


admin.add_view(DanhSachSachView(name="Danh sách sách"))
admin.add_view(NhanVienView(NhanVien, db.session, name="Nhân viên"))
admin.add_view(TheDocGiaView(TheDocGia, db.session, name="Thẻ độc giả"))
admin.add_view(ThongTinSachView(ThongTinSach, db.session, name="Thông tin sách"))
admin.add_view(PhieuMuonSachView(PhieuMuonSach, db.session, name="Phiếu mượn sách"))
admin.add_view(PhieuTraSachView(PhieuTraSach, db.session, name="Phiếu trả sách"))
admin.add_view(PhieuThuTienPhatView(PhieuThuTienPhat, db.session, name="Phiếu thu tiền phạt"))
admin.add_view(GhiNhanMatSachView(GhiNhanMatSach, db.session, name="Ghi nhận mất sách"))
admin.add_view(ThanhLySachView(ThanhLySach, db.session, name="Thanh lý sách"))
admin.add_view(ThongKeView(name="Thống kê"))
admin.add_view(ThoatView(name="Thoát"))
