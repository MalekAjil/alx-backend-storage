-- Create the stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE avg_weighted_score DECIMAL(10,2);
    DECLARE user_id INT;
    DECLARE done INT DEFAULT 0;

    -- Declare a cursor to iterate over all users
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;

    -- Declare a handler for the end of the cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Open the cursor
    OPEN user_cursor;

    -- Loop through all users
    user_loop: LOOP
        -- Fetch the next user_id
        FETCH user_cursor INTO user_id;

        -- Exit the loop if there are no more rows
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Compute the average weighted score for the current user
        SELECT SUM(c.score * p.weight) / SUM(p.weight) INTO avg_weighted_score
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Update the user's average_score attribute
        UPDATE users
        SET average_score = avg_weighted_score
        WHERE id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END //

DELIMITER ;
