CREATE FUNCTION user_insertion_logger() RETURNS TRIGGER AS $$
BEGIN
   RAISE NOTICE 'A new row with id % and username % has been inserted', NEW.userId, NEW.username;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_logger
AFTER INSERT ON users
FOR EACH ROW
EXECUTE PROCEDURE user_insertion_logger();