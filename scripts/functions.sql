
CREATE OR REPLACE FUNCTION fn_SaleQrsToCompany(p_ruc VARCHAR (15),p_period INT, p_numqrs INT, p_userid VARCHAR (100)) 
RETURNS INT AS $$
DECLARE v_packageid package_store.id%TYPE;
BEGIN    
    INSERT INTO package_store (user_id,company_id,num_qrs,due_date,created_by,created_on) 
    VALUES (p_userid,p_ruc,p_numqrs,(NOW() + p_period*interval'1 day'),p_userid,NOW()) 
    RETURNING id INTO v_packageid;

    FOR i IN 1..p_numqrs LOOP
        INSERT INTO uuid_store (qr_uuid,package_id,user_id,created_by,created_on) 
        VALUES (uuid_in(md5((NOW()+i*interval'1 day')::text)::cstring),v_packageid,p_userid,p_userid,NOW());
    END LOOP;

    RETURN 0;
EXCEPTION WHEN OTHERS THEN 
    -- RAISE NOTICE '% %', SQLERRM, SQLSTATE;
    RETURN -1;
END;
$$ LANGUAGE plpgsql;


-- select fn_SaleQrsToCompany('20119288477',60,25,'reynaldomic@gmail.com');