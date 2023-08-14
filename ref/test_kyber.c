#include <stdio.h>
#include <time.h> // Include the time.h library
#include "kem.h"
#include "hex_printer.h"

int main(void)
{
    clock_t start_time, end_time; // Variables to store start and end times

    // Record start time
    start_time = clock();

    // Generate key pair
    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    uint8_t sk[CRYPTO_SECRETKEYBYTES];
    crypto_kem_keypair(pk, sk);

    // Create input message
    uint8_t input_message[] = "Hello kyber dinesh";

    printf("Input Message: %s\n", input_message);

    // Perform key encapsulation
    uint8_t ct[CRYPTO_CIPHERTEXTBYTES];
    uint8_t ss[CRYPTO_BYTES];
    crypto_kem_enc(ct, ss, pk);

    print_hex("Ciphertext", ct, sizeof(ct));
    print_hex("Shared Secret", ss, sizeof(ss));

    // Perform key decapsulation
    uint8_t decrypted_ss[CRYPTO_BYTES];
    crypto_kem_dec(decrypted_ss, ct, sk);

    print_hex("Decrypted Shared Secret", decrypted_ss, sizeof(decrypted_ss));

    // Compare original shared secret with decrypted shared secret
    int success = 1;
    for (size_t i = 0; i < CRYPTO_BYTES; ++i) {
        if (ss[i] != decrypted_ss[i]) {
            success = 0;
            break;
        }
    }

    if (success) {
        printf("Experiment succeeded: Shared secrets match!\n");
    } else {
        printf("Experiment failed: Shared secrets do not match!\n");
    }

    // Record end time
    end_time = clock();

    // Calculate and display the duration
    double duration = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("Time taken: %.6f seconds\n", duration);

    return 0;
}