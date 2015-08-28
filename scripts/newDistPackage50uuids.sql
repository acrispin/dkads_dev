
-- sample assignment qr_uuid to users

DO LANGUAGE plpgsql $$
DECLARE v_userid sy_user.email%TYPE;
DECLARE v_packageid package_store.id%TYPE;
BEGIN
	INSERT INTO sy_user (email, password, name, rol, is_active, created_on)
	VALUES ('ccrispin@gmail.com', '$pbkdf2-sha256$8684$QChFCEEIoVQKQci5l5Iyhg$THMB/xljNCkHPCkoy4ASRP8JOmEmoZHr0IKEOhBxHXc', 'Carlos Crispin', 'dealer', True, NOW())
	RETURNING email INTO v_userid;
    
    FOR i IN 1..50 LOOP
        INSERT INTO uuid_store (qr_uuid,user_id,created_by,created_on) 
        VALUES (uuid_in(md5((NOW()+i*interval'1 day')::text)::cstring),v_userid,v_userid,NOW());
    END LOOP;
END
$$;


DO LANGUAGE plpgsql $$
DECLARE v_userid sy_user.email%TYPE;
BEGIN   
    v_userid = 'reynaldomic@gmail.com';
    FOR i IN 1..23 LOOP
        INSERT INTO uuid_store (qr_uuid,user_id,created_by,created_on) 
        VALUES (uuid_in(md5((NOW()+i*interval'1 day')::text)::cstring),v_userid,v_userid,NOW());
    END LOOP;
END
$$;