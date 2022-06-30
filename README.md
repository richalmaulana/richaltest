# Struktur DB

1. dvd_history_sewa
  - CREATE TABLE public.dvd_history_sewa (
    history_id character varying(20),
    history_id_dvd character varying(20),
    history_id_user character varying(20),
    history_status character varying(5),
    history_feedback character varying(500),
    history_rating character varying(10),
    history_tgl_buat date
  );
 
2. dvd_store_sewa
  - CREATE TABLE public.dvd_store_sewa (
    sewa_id character varying(20),
    sewa_id_dvd character varying(20),
    sewa_id_user character varying(20),
    sewa_tgl_buat date,
    sewa_file character varying(100),
    sewa_status character varying(10),
    sewa_id_update character varying(20),
    sewa_tgl_update date,
    sewa_tgl_pengembalian date
  );

3. dvd_store_test
  - CREATE TABLE public.dvd_store_test (
    dtl_id_dvd character varying(20),
    dtl_judul_film character varying(100),
    dtl_category character varying(20),
    dtl_rating character varying(20),
    dtl_kualitas character varying(100),
    dtl_descp character varying(500),
    dtl_stock character varying(100),
    dtl_user_buat character varying(20),
    dtl_tgl_buat date,
    dtl_user_update character varying(20),
    dtl_tgl_update date,
    dtl_status_aktif character varying(2)
  );
  
4. dvd_store_user
  - CREATE TABLE public.dvd_store_user (
    user_kta character varying(20),
    user_nama character varying(50),
    user_role character varying(5),
    user_pin character varying(10),
    user_aktif character varying(1),
    user_tgl_buat date,
    user_update character varying(20),
    tgl_update date
  );
